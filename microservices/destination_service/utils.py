from typing import List, Dict

PLACES_DB: Dict[str, List[Dict]] = {
    "sightseeing": [
        {"name": "Eiffel Tower", "city": "Paris"},
        {"name": "Louvre Museum", "city": "Paris"},
        {"name": "Colosseum", "city": "Rome"},
        {"name": "Acropolis", "city": "Athens"}
    ],
    "nature": [
        {"name": "Grand Canyon", "city": "Arizona"},
        {"name": "Yellowstone National Park", "city": "Wyoming"},
        {"name": "Banff National Park", "city": "Canada"}
    ],
    "beach": [
        {"name": "Bondi Beach", "city": "Sydney"},
        {"name": "Copacabana", "city": "Rio de Janeiro"},
        {"name": "Waikiki Beach", "city": "Hawaii"}
    ]
}

def get_places(interests: list[str], limit: int = 5):
    places_db = [
        {"name": "Eiffel Tower", "city": "Paris", "country": "FR"},
        {"name": "Acropolis", "city": "Athens", "country": "GR"},
        {"name": "Bondi Beach", "city": "Sydney", "country": "AU"},
        {"name": "Statue of Liberty", "city": "New York", "country": "US"},
        {"name": "Colosseum", "city": "Rome", "country": "IT"},
    ]
    return places_db[:limit]