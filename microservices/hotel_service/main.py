from fastapi import FastAPI, Query
from typing import List, Dict

app = FastAPI(title="Hotel Service")

HOTELS: Dict[str, List[Dict]] = {
     "New York": [
        {"name": "The Plaza Hotel", "stars": 5, "price_per_night": 600},
        {"name": "Pod 51 Hotel", "stars": 3, "price_per_night": 150},
    ],
    "Barcelona": [
        {"name": "Hotel Arts Barcelona", "stars": 5, "price_per_night": 550},
        {"name": "Hostal Girona", "stars": 2, "price_per_night": 80},
    ],
    "Uyuni": [
        {"name": "Hotel Palacio de Sal", "stars": 4, "price_per_night": 200},
        {"name": "Hotel Jardines de Uyuni", "stars": 3, "price_per_night": 90},
    ],
    "Siem Reap": [
        {"name": "Shinta Mani Angkor", "stars": 5, "price_per_night": 250},
        {"name": "Golden Temple Hotel", "stars": 4, "price_per_night": 120},
    ],
    "Moscow": [
        {"name": "Metropol Hotel", "stars": 5, "price_per_night": 400},
        {"name": "Izmailovo Hotel", "stars": 3, "price_per_night": 100},
    ],
    "Mount Athos": [
        {"name": "Monastery Guesthouse", "stars": 3, "price_per_night": 60},
        {"name": "Aristotelis Hotel", "stars": 4, "price_per_night": 110},
    ],
    "Rome": [
        {"name": "Hotel de Russie", "stars": 5, "price_per_night": 500},
        {"name": "Hotel Roma Vaticano", "stars": 3, "price_per_night": 130},
    ],
    "La Spezia": [
        {"name": "The Poet Hotel", "stars": 4, "price_per_night": 180},
        {"name": "CDH Hotel La Spezia", "stars": 3, "price_per_night": 95},
    ],
    "Prague": [
        {"name": "Hotel Kings Court", "stars": 5, "price_per_night": 350},
        {"name": "Mosaic House Hotel", "stars": 4, "price_per_night": 120},
    ],
    "Victoria": [
        {"name": "Fairmont Empress", "stars": 5, "price_per_night": 400},
        {"name": "Strathcona Hotel", "stars": 3, "price_per_night": 110},
    ],
    "Petra": [
        {"name": "Movenpick Resort Petra", "stars": 5, "price_per_night": 220},
        {"name": "Petra Guest House Hotel", "stars": 4, "price_per_night": 130},
    ],
    "Santorini": [
        {"name": "Katikies Hotel", "stars": 5, "price_per_night": 600},
        {"name": "Hotel Thira", "stars": 3, "price_per_night": 90},
    ],
    "Cairns": [
        {"name": "Shangri-La Hotel", "stars": 5, "price_per_night": 280},
        {"name": "Gilligan’s Backpacker Hotel", "stars": 2, "price_per_night": 70},
    ],
    "Rio de Janeiro": [
        {"name": "Copacabana Palace", "stars": 5, "price_per_night": 500},
        {"name": "Hotel Atlantico Prime", "stars": 4, "price_per_night": 120},
    ],
    "Cape Town": [
        {"name": "One&Only Cape Town", "stars": 5, "price_per_night": 450},
        {"name": "The Backpack", "stars": 3, "price_per_night": 80},
    ],
    "Grindavik": [
        {"name": "Northern Light Inn", "stars": 4, "price_per_night": 200},
        {"name": "Harbor View Cottages", "stars": 3, "price_per_night": 120},
    ],
    "Serengeti": [
        {"name": "Serengeti Serena Safari Lodge", "stars": 4, "price_per_night": 300},
        {"name": "Serengeti Sopa Lodge", "stars": 3, "price_per_night": 180},
    ],
    "Moshi": [
        {"name": "Kaliwa Lodge", "stars": 4, "price_per_night": 150},
        {"name": "Mountain Inn", "stars": 3, "price_per_night": 90},
    ],
    "Hilo": [
        {"name": "Grand Naniloa Hotel", "stars": 4, "price_per_night": 210},
        {"name": "Hilo Seaside Hotel", "stars": 3, "price_per_night": 100},
    ],
    "Banff": [
        {"name": "Fairmont Banff Springs", "stars": 5, "price_per_night": 450},
        {"name": "Moose Hotel & Suites", "stars": 4, "price_per_night": 180},
    ],
    "Wyoming": [
        {"name": "Old Faithful Inn", "stars": 4, "price_per_night": 250},
        {"name": "Elk Country Inn", "stars": 3, "price_per_night": 130},
    ],
    "Cusco": [
        {"name": "Palacio del Inka", "stars": 5, "price_per_night": 280},
        {"name": "Hotel Los Andes", "stars": 3, "price_per_night": 90},
    ],
    "Granada": [
        {"name": "Parador de Granada", "stars": 4, "price_per_night": 220},
        {"name": "Hotel Anacapri", "stars": 3, "price_per_night": 95},
    ],
    "Paris": [
        {"name": "Le Meurice", "stars": 5, "price_per_night": 550},
        {"name": "Ibis Paris Montmartre", "stars": 3, "price_per_night": 100},
    ],
    "Cairo": [
        {"name": "Marriott Mena House", "stars": 5, "price_per_night": 320},
        {"name": "Steigenberger Hotel El Tahrir", "stars": 4, "price_per_night": 150},
    ],
    "Fujinomiya": [
        {"name": "Fujinomiya Green Hotel", "stars": 3, "price_per_night": 85},
        {"name": "Super Hotel Fujinomiya", "stars": 2, "price_per_night": 60},
    ],
    "Beijing": [
        {"name": "The Peninsula Beijing", "stars": 5, "price_per_night": 400},
        {"name": "King’s Joy Hotel", "stars": 3, "price_per_night": 80},
    ],
    "Füssen": [
        {"name": "Hotel Sonne", "stars": 4, "price_per_night": 160},
        {"name": "Hotel Hirsch", "stars": 3, "price_per_night": 110},
    ],
    "Alaska": [
        {"name": "Alyeska Resort", "stars": 4, "price_per_night": 230},
        {"name": "Glacier Bay Lodge", "stars": 3, "price_per_night": 140},
    ],
    "Nelspruit": [
        {"name": "Mercure Nelspruit Hotel", "stars": 3, "price_per_night": 100},
        {"name": "Southern Sun Emnotweni", "stars": 4, "price_per_night": 150},
    ],
    "Catania": [
        {"name": "Palace Catania", "stars": 4, "price_per_night": 180},
        {"name": "Hotel Villa Romeo", "stars": 3, "price_per_night": 95},
    ],
    "Grand Canyon": [
        {"name": "El Tovar Hotel", "stars": 4, "price_per_night": 220},
        {"name": "Yavapai Lodge", "stars": 3, "price_per_night": 140},
    ],
    "Niagara Falls": [
        {"name": "Niagara Falls Marriott", "stars": 4, "price_per_night": 250},
        {"name": "Days Inn by Wyndham", "stars": 3, "price_per_night": 120},
    ],
    "Foz do Iguaçu": [
        {"name": "Belmond Hotel das Cataratas", "stars": 5, "price_per_night": 350},
        {"name": "San Juan Eco Hotel", "stars": 4, "price_per_night": 110},
    ],
    "Puerto Ayora": [
        {"name": "Finch Bay Hotel", "stars": 4, "price_per_night": 300},
        {"name": "Hotel Solymar", "stars": 3, "price_per_night": 120},
    ],
    "Dubai": [
        {"name": "Burj Al Arab", "stars": 5, "price_per_night": 1000},
        {"name": "Ibis Al Barsha", "stars": 3, "price_per_night": 90},
    ],
    "Zermatt": [
        {"name": "Mont Cervin Palace", "stars": 5, "price_per_night": 600},
        {"name": "Hotel Alpenhof", "stars": 4, "price_per_night": 200},
    ],
    "Agra": [
        {"name": "The Oberoi Amarvilas", "stars": 5, "price_per_night": 450},
        {"name": "Hotel Taj Resorts", "stars": 3, "price_per_night": 100},
    ],
    "Irkutsk": [
        {"name": "Courtyard by Marriott Irkutsk", "stars": 4, "price_per_night": 150},
        {"name": "Hotel Irkut", "stars": 3, "price_per_night": 90},
    ],
    "Lukla": [
        {"name": "Himalayan Lodge Lukla", "stars": 3, "price_per_night": 60},
        {"name": "Everest Lodge", "stars": 2, "price_per_night": 40},
    ],
    "Istanbul": [
        {"name": "Ciragan Palace Kempinski", "stars": 5, "price_per_night": 400},
        {"name": "Sirkeci Mansion", "stars": 4, "price_per_night": 140},
    ],
    "Amesbury": [
        {"name": "The George Hotel", "stars": 4, "price_per_night": 120},
        {"name": "Stonehenge Inn", "stars": 3, "price_per_night": 80},
    ],
    "Athens": [
        {"name": "Hotel Grande Bretagne", "stars": 5, "price_per_night": 350},
        {"name": "Athens Center Square Hotel", "stars": 3, "price_per_night": 110},
    ],
    "Denizli": [
        {"name": "Richmond Pamukkale Thermal", "stars": 5, "price_per_night": 200},
        {"name": "Venus Suite Hotel", "stars": 3, "price_per_night": 90},
    ],
    "Yucatan": [
        {"name": "Hotel Chichen Itza", "stars": 3, "price_per_night": 85},
        {"name": "Casa de las Columnas", "stars": 4, "price_per_night": 150},
    ],
    "Sydney": [
        {"name": "Park Hyatt Sydney", "stars": 5, "price_per_night": 600},
        {"name": "Ibis Sydney World Square", "stars": 3, "price_per_night": 100},
    ],
    "Versailles": [
        {"name": "Trianon Palace Versailles", "stars": 5, "price_per_night": 300},
        {"name": "Hotel du Cheval Rouge", "stars": 3, "price_per_night": 120},
    ],
}


@app.get("/hotels")
async def get_hotels(city: str = Query(..., description="Название города")):
    hotels = HOTELS.get(city)
    if hotels:
        return {"city": city, "hotels": hotels}
    return {"city": city, "hotels": [], "message": "Нет данных для этого города"}
