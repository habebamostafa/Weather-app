import requests
import pandas as pd
import streamlit as st

def reverse_geocode(lat, lon):
    url = f"https://geocoding-api.open-meteo.com/v1/reverse?latitude={lat}&longitude={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["name"]
    return f"{lat},{lon}"  # fallback

def get_coordinates(city_input):
    if "," in city_input:
        try:
            lat, lon = map(float, city_input.split(","))
            city_name = reverse_geocode(lat, lon)
            return lat, lon, city_name
        except ValueError:
            return None, None, None
    else:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_input}&count=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"], result["name"]
    return None, None, None

def get_weather(city_input):
    lat, lon, validated_city = get_coordinates(city_input)
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


def get_forecast(city_input):
    lat, lon, validated_city = get_coordinates(city_input)
    if lat is None or lon is None:
        return None
    
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
    
    return None