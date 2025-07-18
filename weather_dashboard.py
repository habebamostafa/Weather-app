import streamlit as st
import requests
import pandas as pd
import sqlite3
from datetime import datetime

DB_NAME = "weather.db"

# ===================== DB Setup =====================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        temperature REAL,
        weather TEXT
    )''')
    conn.commit()
    conn.close()

# ===================== API Functions =====================
def get_weather(city):
    try:
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geocode_url).json()
        if not geo_res.get("results"):
            return None

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,weathercode&timezone=auto"
        weather_res = requests.get(forecast_url).json()
        days = weather_res["daily"]

        forecast = []
        for i in range(len(days["time"])):
            forecast.append({
                "city": city,
                "date": days["time"][i],
                "temperature": days["temperature_2m_max"][i],
                "weather": get_weather_icon(days["weathercode"][i])
            })
        return forecast
    except:
        return None

def get_weather_icon(code):
    # simplified weather codes
    code = int(code)
    if code == 0:
        return "☀️ Clear"
    elif code in [1, 2, 3]:
        return "⛅️ Partly Cloudy"
    elif code in [45, 48]:
        return "🌫️ Fog"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "🌧️ Rain"
    elif code in [71, 73, 75, 85, 86]:
        return "❄️ Snow"
    elif code in [95, 96, 99]:
        return "⛈️ Thunderstorm"
    else:
        return "🌡️ N/A"

# ===================== DB Functions =====================
def save_to_db(forecast):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for entry in forecast:
        cursor.execute("INSERT INTO weather_data (city, date, temperature, weather) VALUES (?, ?, ?, ?)",
                       (entry['city'], entry['date'], entry['temperature'], entry['weather']))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather_data WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def update_record(record_id, new_city, new_date, new_temp, new_weather):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""UPDATE weather_data 
                      SET city=?, date=?, temperature=?, weather=? 
                      WHERE id=?""",
                   (new_city, new_date, new_temp, new_weather, record_id))
    conn.commit()
    conn.close()

# ===================== UI App =====================
st.set_page_config(page_title="🌍 Weather Dashboard", layout="centered")
st.title("🌦️ Smart Weather Dashboard")

init_db()

# Tab layout
tab1, tab2, tab3 = st.tabs(["🔍 Get Weather", "📋 View & Manage Data", "⬇️ Export"])

# 1. Get Weather
with tab1:
    city = st.text_input("Enter City Name:")
    if st.button("Get Forecast"):
        forecast = get_weather(city)
        if forecast:
            st.success(f"Showing 5-Day Forecast for {city}")
            df = pd.DataFrame(forecast)
            st.dataframe(df)
            if st.button("Save to Database"):
                save_to_db(forecast)
                st.success("Data Saved to DB ✅")
        else:
            st.error("City not found or API error.")

# 2. View/Update/Delete Data
with tab2:
    df = fetch_all()
    st.dataframe(df)

    st.subheader("🧽 Delete Record")
    id_to_delete = st.number_input("Enter Record ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        delete_record(id_to_delete)
        st.success("Deleted ✅")

    st.subheader("✏️ Update Record")
    id_to_update = st.number_input("Record ID", min_value=1, step=1, key="update_id")
    new_city = st.text_input("New City", key="update_city")
    new_date = st.text_input("New Date (yyyy-mm-dd)", key="update_date")
    new_temp = st.number_input("New Temp", key="update_temp")
    new_weather = st.text_input("New Weather Description", key="update_weather")

    if st.button("Update"):
        update_record(id_to_update, new_city, new_date, new_temp, new_weather)
        st.success("Updated ✅")

# 3. Export Data
with tab3:
    df = fetch_all()
    st.subheader("📥 Download Data")
    csv = df.to_csv(index=False).encode()
    json = df.to_json(orient="records").encode()

    st.download_button("Download as CSV", csv, "weather_data.csv", "text/csv")
    st.download_button("Download as JSON", json, "weather_data.json", "application/json")
