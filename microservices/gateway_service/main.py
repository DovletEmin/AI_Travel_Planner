from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

DESTINATION_URL = os.getenv("DESTINATION_URL", "http://127.0.0.1:8001/destinations")
WEATHER_URL = os.getenv("WEATHER_URL", "http://127.0.0.1:8002/weather")
HOTEL_URL = os.getenv("HOTEL_URL", "http://127.0.0.1:8003/hotels")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10.0"))

app = FastAPI(title="Gateway / Trip Planner")

class PlanRequest(BaseModel):
    interests: List[str]
    limit: int = 5
    min_temp: Optional[float] = None
    max_temp: Optional[float] = None
    weather_contains: Optional[str] = None

async def fetch_weather_for_city(client: httpx.AsyncClient, city: str) -> Dict[str, Any]:
    try:
        resp = await client.get(WEATHER_URL, params={"city": city}, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return {"error": f"no weather for {city}"}
        else:
            return {"error": f"weather service returned {resp.status_code}"}
    except httpx.RequestError as e:
        return {"error": f"weather service unreachable: {e}"}

async def fetch_hotels_for_city(client: httpx.AsyncClient, city: str) -> List[Dict[str, Any]]:
    try:
        resp = await client.get(HOTEL_URL, params={"city": city}, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json().get("hotels", [])
        else:
            return []
    except httpx.RequestError:
        return []

@app.post("/plan")
async def plan_trip(req: PlanRequest):
    params = [("interests", it) for it in req.interests]
    params.append(("limit", str(req.limit)))

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(DESTINATION_URL, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Destination service unreachable: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Destination service error: {e.response.text}")

        data = resp.json()
        places = data.get("destinations", [])

        weather_tasks = [fetch_weather_for_city(client, place.get("city", "")) for place in places]
        hotel_tasks = [fetch_hotels_for_city(client, place.get("city", "")) for place in places]

        weathers, hotels_list = await asyncio.gather(
            asyncio.gather(*weather_tasks),
            asyncio.gather(*hotel_tasks)
        )

        for place, weather, hotels in zip(places, weathers, hotels_list):
            place["weather"] = weather
            place["hotels"] = hotels

        def passes_filters(place: Dict) -> bool:
            w = place.get("weather", {})
            temp = w.get("temperature")
            if temp is not None:
                if req.min_temp is not None and temp < req.min_temp:
                    return False
                if req.max_temp is not None and temp > req.max_temp:
                    return False
            if req.weather_contains:
                desc = (w.get("description") or "").lower()
                if req.weather_contains.lower() not in desc:
                    return False
            return True

        filtered = [p for p in places if passes_filters(p)]
        return {"plan": filtered}
