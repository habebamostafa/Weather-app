import streamlit as st
from db import create_table, insert_weather_data, fetch_all_data
from weather_util import get_weather
import pandas as pd

# إنشاء الجدول لو مش موجود
create_table()

st.title("🌤️ Weather Tracker App")
st.write("احصل على حالة الطقس واحفظها")

city = st.text_input("أدخل اسم المدينة", "Cairo")

if st.button("جلب حالة الطقس"):
    temperature, windspeed = get_weather(city)
    if temperature is not None:
        insert_weather_data(city, temperature, windspeed)
        st.success(f"✔ تم حفظ بيانات الطقس لـ {city}")
        st.write(f"🌡️ درجة الحرارة: {temperature}°C")
        st.write(f"💨 سرعة الرياح: {windspeed} km/h")
    else:
        st.error("❌ فشل في جلب البيانات. حاول مرة أخرى")

if st.button("📜 عرض كل البيانات"):
    rows = fetch_all_data()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "City", "Temperature", "Wind Speed", "Timestamp"])
        st.dataframe(df)
        st.download_button("📥 تحميل CSV", df.to_csv(index=False), "weather_data.csv", "text/csv")
    else:
        st.info("لا توجد بيانات محفوظة حتى الآن.")
