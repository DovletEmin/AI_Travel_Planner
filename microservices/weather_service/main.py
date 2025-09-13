# weather_service/main.py
from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict, Tuple
import time

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

app = FastAPI(title="Weather Service")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise RuntimeError("Please set OPENWEATHER_API_KEY in .env")

_WEATHER_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"
_GEOCODING_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"

_GEO_CACHE: Dict[str, Tuple[float, Dict[str, float]]] = {}
GEO_CACHE_TTL = int(os.getenv("GEO_CACHE_TTL", "86400"))


def _get_cached_coords(city: str) -> Optional[Dict[str, float]]:
    key = city.strip().lower()
    item = _GEO_CACHE.get(key)
    if not item:
        return None
    ts, coords = item
    if time.time() - ts < GEO_CACHE_TTL:
        return coords
    _GEO_CACHE.pop(key, None)
    return None


def _cache_coords(city: str, coords: Dict[str, float]) -> None:
    key = city.strip().lower()
    _GEO_CACHE[key] = (time.time(), coords)


def geocode_city(city: str) -> Optional[Dict[str, float]]:
    cached = _get_cached_coords(city)
    if cached:
        return cached

    params = {"q": city, "limit": 1, "appid": OPENWEATHER_API_KEY}
    try:
        resp = requests.get(_GEOCODING_ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    data = resp.json()
    if not data:
        return None

    first = data[0]
    lat = first.get("lat")
    lon = first.get("lon")
    if lat is None or lon is None:
        return None

    coords = {"lat": lat, "lon": lon}
    _cache_coords(city, coords)
    return coords


@app.get("/weather")
def get_weather(city: str):
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="Parameter 'city' is required")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "en",
    }

    try:
        resp = requests.get(_WEATHER_ENDPOINT, params=params, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Weather API request failed: {e}")

    if resp.status_code == 200:
        data = resp.json()
        return {
            # "source": "q",
            # "city": data.get("name") or city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }

    if resp.status_code == 404:
        coords = geocode_city(city)
        if not coords:
            raise HTTPException(status_code=404, detail=f"City not found: {city}")

        params_coords = {
            "lat": coords["lat"],
            "lon": coords["lon"],
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "en",
        }
        try:
            resp2 = requests.get(_WEATHER_ENDPOINT, params=params_coords, timeout=10)
            resp2.raise_for_status()
        except requests.HTTPError as e:
            raise HTTPException(status_code=resp2.status_code if resp2 is not None else 502,
                                detail=f"Weather API error for coords: {e}")
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Weather API request failed for coords: {e}")

        data2 = resp2.json()
        return {
            # "source": "geocoding->coords",
            # "city": data2.get("name") or city,
            "temperature": data2["main"]["temp"],
            "description": data2["weather"][0]["description"],
            "coords": coords,
        }

    raise HTTPException(status_code=502, detail=f"Weather API returned status {resp.status_code}: {resp.text}")
