import os
from fastapi import FastAPI, Query
import httpx
from dotenv import load_dotenv

from . import utils

load_dotenv()

app = FastAPI()

WEATHER_SERVICE_URL = os.getenv("WEATHER_SERVICE_URL", "http://127.0.0.1:8002/weather")

@app.get("/destinations")
async def get_destinations(
    interests: list[str] = Query(..., description="Список интересов, например: history, beach"),
    limit: int = Query(5, description="Максимум мест в выдаче"),
):
    destinations = utils.get_places(interests, limit)
    results = []

    async with httpx.AsyncClient() as client:
        for place in destinations:
            city = place["city"]
            try:
                r = await client.get(f"{WEATHER_SERVICE_URL}?city={city}")
                if r.status_code == 200:
                    weather = r.json()
                else:
                    weather = {"message": f"нет данных для {city}"}
            except Exception as e:
                weather = {"message": f"ошибка сервиса погоды: {e}"}

            results.append({
                "name": place["name"],
                "city": city,
                "weather": weather
            })

    return {"destinations": results}
