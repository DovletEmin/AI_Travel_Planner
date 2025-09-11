from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx

from .utils import get_places


app = FastAPI(title="Destination Service")

class DestinationRequest(BaseModel):
    interests: List[str]
    limit: int = 5

class DestinationResponse(BaseModel):
    name: str
    city: str
    weather: dict | None = None

@app.post("/destinations")
async def get_destinations(payload: DestinationRequest):
    places = get_places(payload.interests, payload.limit)

    async with httpx.AsyncClient() as client:
        for place in places:
            try:
                resp = await client.get(
                    "http://127.0.0.1:8001/weather",
                    params={"city": place["city"]}
                )
                resp.raise_for_status()
                place["weather"] = resp.json()
            except httpx.RequestError:
                place["weather"] = {"error": "Weather service unreachable"}
            except httpx.HTTPStatusError:
                place["weather"] = {"error": "Weather not found"}

    return {"destinations": places}