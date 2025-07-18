import streamlit as st
import pandas as pd
from db import create_table, insert_weather_data, fetch_all_data, update_record, delete_record
from weather_util import get_coordinates, get_weather, get_forecast
from streamlit_folium import st_folium
import folium
st.set_page_config(page_title="🌦️ Weather Tracker by Habeba Mostafa", layout="centered")

create_table()
st.title("🌤️ Weather Tracker App")
st.info("Created by Habeba Mostafa | Info: PM Accelerator trains future PMs → [Product Manager Accelerator]")

input_type = st.selectbox("🗺️ Select input type:", ["City Name", "Zip Code / Postal Code", "GPS Coordinates", "Landmark"])
city_input = st.text_input("Enter a city name or coordinates (lat,lon):", value="Cairo")

if city_input:
    city_name, temp, wind = get_weather(city_input)
    forecast_df = get_forecast(city_input)

    coords = get_coordinates(city_input)
    if coords:
        lat, lon,_ = coords
    else:
        st.error("❌ Could not find location coordinates.")
        st.stop()

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("🗺️ Location on Map")
        map_ = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], tooltip=city_name.title()).add_to(map_)
        st_data = st_folium(map_, width=350, height=350)

    with col2:
        if city_name and temp is not None:
            st.subheader(f"🌡️ Current Weather in {city_name}")
            st.metric("Temperature (°C)", f"{temp}°C")
            st.metric("Wind Speed (km/h)", f"{wind} km/h")
        else:
            st.error("❌ Couldn't retrieve current weather.")

    if forecast_df is not None:
        st.subheader(f"📅 5-Day Forecast for {forecast_df['City'][0]}")
        st.dataframe(forecast_df)
    
    else:
        st.error("❌ Couldn't retrieve forecast data.")

def process_input(input_type, user_input):
    if input_type in ["Landmark", "GPS Coordinates"]:
        coords = get_coordinates(user_input)
        if coords:
            return f"{coords[0]},{coords[1]}"
        else:
            return None
    else:
        return user_input

# --- Data Management Section ---
st.markdown("---")
st.subheader("📚 Manage Weather Records")

rows = fetch_all_data()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "City", "Temperature", "Wind Speed", "Timestamp"])
    st.dataframe(df)

    export = st.radio("Download data as:", ("CSV", "JSON"))
    if export == "CSV":
        st.download_button("📥 Download CSV", df.to_csv(index=False), "weather.csv", "text/csv")
    else:
        st.download_button("📥 Download JSON", df.to_json(orient="records"), "weather.json", "application/json")

    with st.expander("✏️ Update or 🗑️ Delete a Record"):
        record_id = st.number_input("Record ID", min_value=1, step=1)
        new_temp = st.number_input("New Temperature", step=0.1)
        if st.button("Update"):
            update_record(record_id, new_temp)
            st.success("✅ Record updated successfully.")
        if st.button("Delete"):
            delete_record(record_id)
            st.warning("🗑️ Record deleted.")
else:
    st.info("No records available yet.")
