from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

app = FastAPI(title="Weather Service")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise RuntimeError("Please set OPENWEATHER_API_KEY in .env")


@app.get("/weather")
def get_weather(city: str, country: str | None = None):
    query = f"{city},{country}" if country else city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={quote(query)}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    print("DEBUG URL:", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {e}")

    data = response.json()
    return {
        "city": city,
        "country": country,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }