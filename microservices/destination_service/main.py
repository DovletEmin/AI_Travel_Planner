from fastapi import FastAPI, Query
from typing import List
from . import utils

app = FastAPI(title="Destination Service")

@app.get("/destinations")
async def get_destinations(
    interests: List[str] = Query(..., description="Список интересов, например: history, beach"),
    limit: int = Query(5, description="Максимум мест в выдаче"),
):
    places = utils.get_places(interests, limit)
    return {"destinations": places}
