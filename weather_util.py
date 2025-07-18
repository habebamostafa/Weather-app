import requests

def get_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=30.0444&longitude=31.2357&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        temperature = weather["temperature"]
        windspeed = weather["windspeed"]
        return temperature, windspeed
    else:
        return None, None
