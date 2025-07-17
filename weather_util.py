import requests

def get_weather_forecast(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"
