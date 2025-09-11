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

def get_places(interests: List[str], limit: int = 5) -> List[Dict]:
    results = []
    for interest in interests:
        results.extend(PLACES_DB.get(interest, []))
    return results[:limit]
