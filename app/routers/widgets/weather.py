from fastapi import APIRouter, HTTPException
import httpx


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Light rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail"
}
router = APIRouter(prefix="/widgets/weather")

@router.get("/")
def get_weather(city: str):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = httpx.get("https://geocoding-api.open-meteo.com/v1/search", params=params)
    data = response.json()
    
    # if city doesn't exist
    if not data.get("results"):
        raise HTTPException(status_code=404, detail="City not found")

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code"
    }

    weather_response = httpx.get("https://api.open-meteo.com/v1/forecast", params=weather_params)
    weather_data = weather_response.json()

    temperature = weather_data["current"]["temperature_2m"]
    weather_code = weather_data["current"]["weather_code"]
    condition = WEATHER_CODES.get(weather_code, "Unknown")

    return {
        "city": city,
        "temperature": temperature,
        "weather_code": condition
    }