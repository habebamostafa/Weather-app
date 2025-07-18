import streamlit as st
from weather_util import get_coordinates, get_weather

st.title("🌤️ Dynamic Weather App")

city = st.text_input("Enter a city name:")

if city:
    lat, lon = get_coordinates(city)
    if lat and lon:
        temperature, windspeed = get_weather(lat, lon)
        if temperature is not None:
            st.success(f"📍 Location: {city}\n\n🌡️ Temperature: {temperature}°C\n💨 Wind Speed: {windspeed} km/h")
        else:
            st.error("Couldn't fetch weather data. Try again later.")
    else:
        st.error("City not found. Please check the spelling.")
