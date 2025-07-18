import streamlit as st
import pandas as pd
from db import create_table, insert_weather_data, fetch_all_data, update_record, delete_record
from weather_util import get_coordinates, get_weather, get_forecast

st.set_page_config(page_title="🌦️ Weather Tracker by [Your Name]", layout="centered")

create_table()
st.title("🌤️ Weather Tracker App")
st.info("Created by [Your Name] | Info: PM Accelerator trains future PMs → [Product Manager Accelerator](https://www.linkedin.com/company/product-manager-accelerator/)")

city_name = st.text_input("أدخل اسم المدينة:")

if st.button("احصل على الطقس"):
    if city_name.strip() == "":
        st.warning("من فضلك أدخل اسم مدينة.")
    else:
        city, temperature, windspeed = get_weather(city_name)
        if city:
            insert_weather_data(city, temperature, windspeed)
            st.success(f"📍 المدينة: {city}\n\n🌡️ درجة الحرارة: {temperature}°C\n💨 سرعة الرياح: {windspeed} km/h")
        else:
            st.error("❌ لا توجد مدينة بهذا الاسم. حاول مرة أخرى.")
        
if st.button("📆 عرض توقعات 5 أيام"):
    if city_name.strip() == "":
        st.warning("من فضلك أدخل اسم مدينة.")
    else:
        forecast_df = get_forecast(city_name)
        if forecast_df is not None and not forecast_df.empty:
            st.subheader(f"📅 التوقعات الجوية لـ 5 أيام في مدينة {forecast_df['City'][0]}")
            st.dataframe(forecast_df)
            st.download_button("📥 تحميل CSV", forecast_df.to_csv(index=False), "5_day_forecast.csv", "text/csv")
        else:
            st.error("❌ لا توجد مدينة بهذا الاسم أو فشل في جلب التوقعات.")

st.markdown("---")
st.subheader("📚 إدارة البيانات")

rows = fetch_all_data()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "المدينة", "درجة الحرارة", "سرعة الرياح", "الوقت"])
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