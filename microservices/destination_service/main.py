from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import httpx
import asyncio
import os
import time

from .utils import get_places  

app = FastAPI(title="Destination Service")

WEATHER_URL = os.getenv("WEATHER_URL", "http://127.0.0.1:8001/weather")
_WEATHER_CACHE: Dict[str, tuple[float, dict]] = {}
CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL", "600"))  # seconds, default 10 minutes


class DestinationRequest(BaseModel):
    interests: List[str]
    limit: int = 5


@app.post("/destinations")
async def get_destinations(payload: DestinationRequest):
    places = get_places(payload.interests, payload.limit)

    async with httpx.AsyncClient() as client:
        tasks = [fetch_weather_for_place(client, place) for place in places]
        results = await asyncio.gather(*tasks)

    return {"destinations": results}


async def fetch_weather_for_place(client: httpx.AsyncClient, place: dict) -> dict:
    city = place.get("city")
    country = place.get("country")
    if not city:
        place["weather"] = {"error": "no city provided"}
        return place

    now = time.time()
    cached = _WEATHER_CACHE.get(city.lower())
    if cached:
        ts, data = cached
        if now - ts < CACHE_TTL:
            place["weather"] = data
            return place
        else:
            _WEATHER_CACHE.pop(city.lower(), None)

    try:
        resp = await client.get(
            WEATHER_URL,
            params={"city": city, "country": country},  # Передаем country
            timeout=10.0
        )
        resp.raise_for_status()
        data = resp.json()
        _WEATHER_CACHE[city.lower()] = (now, data)
        place["weather"] = data
    except httpx.HTTPStatusError as e:
        place["weather"] = {"error": f"weather service error: {e.response.status_code}"}
    except httpx.RequestError as e:
        place["weather"] = {"error": f"weather service unreachable: {str(e)}"}
    except Exception as e:
        place["weather"] = {"error": f"unexpected error: {str(e)}"}

    return place