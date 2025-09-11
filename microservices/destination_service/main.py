from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from .utils import get_places


app = FastAPI(title="Destination Service")

class DestinationRequest(BaseModel):
    interests: List[str]
    limit: int = 5

@app.post("/destinations")
def get_destination(payload: DestinationRequest):
    places = get_places(payload.interests, payload.limit)
    return {"destinations": places}