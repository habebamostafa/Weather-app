import requests
import pandas as pd

def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json&limit=1"
    headers = {"User-Agent": "weather-app"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if len(data) > 0 and "lat" in data[0] and "lon" in data[0]:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            display_name = data[0]["display_name"]
            return latitude, longitude, display_name
        else:
            return None, None, None
    else:
        return None, None, None


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
