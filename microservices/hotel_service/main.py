from fastapi import FastAPI, Query
import requests
import os


app = FastAPI()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
HOTEL_API_URL = "https://hotels4.p.rapidapi.com/locations/v3/search"

HEADERS = {
    "x-rapidapi-host": "hotels4.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

@app.get("/hotels")
def get_hotels(city: str = Query(..., description="Название города")):
    querystring = {"q": city, "locale": "en_US"}
    response = requests.get(HOTEL_API_URL, headers=HEADERS, params=querystring)

    if response.status_code != 200:
        return {"error": "Failed to fetch hotels"}
    
    data = response.json()
    hotels = []
    for h in data.get("sr", [])[:5]:
        hotels.append({
            "name": h.get("regionNames", {}).get("fullname"),
            "type": h.get("type"),
            "id": h.get("gaiaId")
        })
    return {"city": city, "hotels": hotels}