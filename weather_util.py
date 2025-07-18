import requests
import pandas as pd

import requests

REVERSE_GEOCODE_API = "https://nominatim.openstreetmap.org/reverse"

def get_coordinates(location_input):
    location_input = location_input.strip()

    if "," in location_input:
        parts = location_input.split(",")
        if len(parts) == 2:
            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    place_name = get_place_name_from_coordinates(lat, lon)
                    return lat, lon, place_name or f"Coordinates ({lat},{lon})"
            except ValueError:
                pass

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_input}&count=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return result["latitude"], result["longitude"], result["name"]

    return None, None, None


def get_place_name_from_coordinates(lat, lon):
    try:
        response = requests.get(REVERSE_GEOCODE_API, params={
            "format": "json",
            "lat": lat,
            "lon": lon
        }, headers={"User-Agent": "weather-app"})
        
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name")
    except Exception as e:
        print("Error in reverse geocoding:", e)
    return None

def get_weather(location_input):
    lat, lon, validated_location = get_coordinates(location_input)
    if lat is None or lon is None:
        return None, None, None

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        temperature = weather["temperature"]
        windspeed = weather["windspeed"]
        return validated_location, temperature, windspeed
    return None, None, None


def get_forecast(location_input):
    lat, lon, validated_location = get_coordinates(location_input)
    if lat is None or lon is None:
        return None  # Invalid input

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
            df.insert(0, "Location", validated_location)
            return df.head(5)

    return None
