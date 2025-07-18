import streamlit as st
import pandas as pd
from db import create_table, insert_weather_data, fetch_all_data, update_record, delete_record
from weather_util import get_coordinates, get_weather, get_forecast

st.set_page_config(page_title="🌦️ Weather Tracker by [Your Name]", layout="centered")

create_table()
st.title("🌤️ Weather Tracker App")
st.info("Created by [Your Name] | Info: PM Accelerator trains future PMs → [Product Manager Accelerator](https://www.linkedin.com/company/product-manager-accelerator/)")

city = st.text_input("أدخل اسم المدينة (أو موقع آخر)")

if st.button("📍 جلب الطقس الحالي"):
    lat, lon = get_coordinates(city)
    if lat and lon:
        temperature, windspeed = get_weather(lat, lon)
        if temperature:
            insert_weather_data(city, temperature, windspeed)
            st.success(f"✔ الطقس الحالي لـ {city}")
            st.write(f"🌡️ درجة الحرارة: {temperature}°C")
            st.write(f"💨 سرعة الرياح: {windspeed} كم/س")
        else:
            st.error("⚠️ فشل في جلب الطقس")
    else:
        st.error("⚠️ لم يتم العثور على الموقع")

if st.button("📆 عرض توقعات 5 أيام"):
    lat, lon = get_coordinates(city)
    if lat and lon:
        forecast_df = get_forecast(lat, lon)
        st.dataframe(forecast_df)
        st.download_button("📥 تحميل CSV", forecast_df.to_csv(index=False), "5_day_forecast.csv", "text/csv")
    else:
        st.error("⚠️ لم يتم العثور على الموقع")

st.markdown("---")
st.subheader("📚 إدارة البيانات")

rows = fetch_all_data()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "City", "Temperature", "Wind Speed", "Timestamp"])
    st.dataframe(df)
    export = st.radio("تنزيل البيانات بصيغة", ("CSV", "JSON"))
    if export == "CSV":
        st.download_button("📥 CSV", df.to_csv(index=False), "weather.csv", "text/csv")
    else:
        st.download_button("📥 JSON", df.to_json(orient="records"), "weather.json", "application/json")

    with st.expander("✏️ تعديل أو 🗑 حذف سجل"):
        record_id = st.number_input("رقم السجل", min_value=1, step=1)
        new_temp = st.number_input("درجة حرارة جديدة", step=0.1)
        if st.button("تعديل"):
            update_record(record_id, new_temp)
            st.success("✅ تم التعديل")
        if st.button("حذف"):
            delete_record(record_id)
            st.warning("🗑 تم الحذف")
else:
    st.info("لا توجد بيانات بعد")