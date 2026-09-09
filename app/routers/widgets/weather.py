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

# helper function to deal with timeout
def fetch_api(url: str, params: dict):
    try:
        response = httpx.get(url, params=params, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="Weather service is unavailable")


@router.get("/")
def get_weather(city: str):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    data = fetch_api("https://geocoding-api.open-meteo.com/v1/search", params)

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
    
    
    weather_data = fetch_api("https://api.open-meteo.com/v1/forecast", weather_params)

    temperature = weather_data["current"]["temperature_2m"]
    weather_code = weather_data["current"]["weather_code"]
    condition = WEATHER_CODES.get(weather_code, "Unknown")

    return {
        "city": city,
        "temperature": temperature,
        "condition": condition
    }