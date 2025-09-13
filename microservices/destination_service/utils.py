from typing import List, Dict

PLACES_DB: List[Dict] = [
    {"name": "Eiffel Tower", "city": "Paris", "country": "FR", "tags": ["history", "architecture"]},
    {"name": "Louvre Museum", "city": "Paris", "country": "FR", "tags": ["museum", "art"]},
    {"name": "Colosseum", "city": "Rome", "country": "IT", "tags": ["history", "architecture"]},
    {"name": "Acropolis", "city": "Athens", "country": "GR", "tags": ["history", "culture"]},
    {"name": "Bondi Beach", "city": "Sydney", "country": "AU", "tags": ["beach", "surfing"]},
    {"name": "Statue of Liberty", "city": "New York", "country": "US", "tags": ["history", "monument"]},
    {"name": "Mount Fuji", "city": "Fujinomiya", "country": "JP", "tags": ["nature", "mountain"]},
    {"name": "Grand Canyon", "city": "Grand Canyon", "country": "US", "tags": ["nature", "park"]},
]

def get_places(interests: List[str], limit: int = 5) -> List[Dict]:
    interests_set = set(i.lower() for i in interests)
    filtered = [p for p in PLACES_DB if interests_set & set(t.lower() for t in p.get("tags", []))]
    return filtered[:limit]
