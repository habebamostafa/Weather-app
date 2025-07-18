import requests
import pandas as pd

def get_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    r = requests.get(url, headers={"User-Agent": "weather-app"})
    if r.status_code == 200 and r.json():
        data = r.json()[0]
        return float(data['lat']), float(data['lon'])
    return None, None

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()["current_weather"]
        return data["temperature"], data["windspeed"]
    return None, None

def get_forecast(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    r = requests.get(url)
    if r.status_code == 200:
        daily = r.json()["daily"]
        df = pd.DataFrame({
            "Date": daily["time"],
            "Max Temp": daily["temperature_2m_max"],
            "Min Temp": daily["temperature_2m_min"]
        })
        return df.head(5)
    return pd.DataFrame()
