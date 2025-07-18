import requests
import pandas as pd

def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return result["latitude"], result["longitude"], result["name"]
    return None, None, None


def get_weather(city_name):
    lat, lon, validated_city = get_coordinates(city_name)
    if lat is None or lon is None:
        return None ,None,None
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        temperature = weather["temperature"]
        windspeed = weather["windspeed"]
        return validated_city, temperature, windspeed
    return None, None, None

def get_forecast(city_name):
    lat, lon, validated_city = get_coordinates(city_name)
    if lat is None or lon is None:
        return None  # مدينة غير صالحة
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    )
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        daily = data.get("daily", {})
        if "time" in daily and "temperature_2m_max" in daily and "temperature_2m_min" in daily:
            df = pd.DataFrame({
                "Date": daily["time"],
                "Max Temperature (°C)": daily["temperature_2m_max"],
                "Min Temperature (°C)": daily["temperature_2m_min"]
            })
            df.insert(0, "City", validated_city)
            return df.head(5)
    
    return None  # فشل في جلب البيانات
