import streamlit as st
import requests
import datetime
from db import add_weather_data, get_all_data,init_db
init_db()
st.set_page_config(page_title="Weather App", layout="centered")
st.title("🌦️Open-Meteo API")

city = st.text_input("أدخل المدينة (بالإنجليزية):", "Cairo")

# عند الضغط على زر "جلب البيانات"
if st.button("عرض الطقس"):
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geocoding_url).json()

    if "results" in geo_res and geo_res["results"]:
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )
        weather_res = requests.get(weather_url).json()

        if "current_weather" in weather_res:
            weather = weather_res["current_weather"]
            temperature = weather["temperature"]
            windspeed = weather["windspeed"]
            time = weather["time"]

            st.success(f"🌍 الموقع: {city}")
            st.write(f"🌡️ درجة الحرارة: {temperature} °C")
            st.write(f"💨 سرعة الرياح: {windspeed} km/h")
            st.write(f"⏰ التوقيت: {time}")

            # حفظ البيانات في قاعدة البيانات
            add_weather_data(city, temperature, windspeed, time)
        else:
            st.error("❌ لم يتم العثور على بيانات الطقس.")
    else:
        st.error("❌ لم يتم العثور على المدينة.")

# عرض البيانات المحفوظة
if st.checkbox("عرض كل البيانات المحفوظة"):
    rows = get_all_data()
    for row in rows:
        st.write(f"📍 {row[1]} | 🌡️ {row[2]} °C | 💨 {row[3]} km/h | 🕒 {row[4]}")
