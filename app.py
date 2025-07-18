import streamlit as st
import pandas as pd
from db import create_table, insert_weather_data, fetch_all_data, update_record, delete_record
from weather_util import get_coordinates, get_weather, get_forecast

st.set_page_config(page_title="🌦️ Weather Tracker by Habeba Mostafa", layout="centered")

create_table()
st.title("🌤️ Weather Tracker App")
st.info("Created by Habeba Mostafa | Info: PM Accelerator trains future PMs → [Product Manager Accelerator]")

input_type = st.selectbox("🗺️ Select input type:", ["City Name", "Zip Code / Postal Code", "GPS Coordinates", "Landmark"])
city_input = st.text_input("Enter a city name or coordinates (lat,lon):", value="Cairo")

if city_input:
    city_name, temp, wind = get_weather(city_input)
    forecast_df = get_forecast(city_input)

    if city_name and temp is not None:
        st.subheader(f"🌡️ Current Weather in {city_name}")
        st.write(f"**Temperature:** {temp} °C")
        st.write(f"**Wind Speed:** {wind} km/h")
    else:
        st.error("❌ Couldn't retrieve current weather. Please check your input.")

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

# --- Get Weather Button ---
if st.button("🌡️ Get Current Weather"):
    if city_input.strip() == "":
        st.warning("Please enter a valid input.")
    else:
        location_query = process_input(input_type, city_input)
        if location_query:
            city, temperature, windspeed = get_weather(location_query)
            if city:
                insert_weather_data(city, temperature, windspeed)
                st.success(f"📍 City: {city}\n\n🌡️ Temperature: {temperature}°C\n💨 Wind Speed: {windspeed} km/h")
            else:
                st.error("❌ Could not fetch weather for the provided input.")
        else:
            st.error("❌ Could not geocode the input.")

# --- Forecast Button ---
if st.button("📆 Show 5-Day Forecast"):
    if city_input.strip() == "":
        st.warning("Please enter a valid input.")
    else:
        location_query = process_input(input_type, city_input)
        if location_query:
            forecast_df = get_forecast(location_query)
            if forecast_df is not None and not forecast_df.empty:
                st.subheader(f"📅 5-Day Forecast for {forecast_df['City'][0]}")
                st.dataframe(forecast_df)
                st.download_button("📥 Download CSV", forecast_df.to_csv(index=False), "5_day_forecast.csv", "text/csv")
            else:
                st.error("❌ Failed to fetch forecast.")
        else:
            st.error("❌ Could not geocode the input.")

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
