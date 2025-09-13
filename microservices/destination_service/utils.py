def get_places(interests: list[str], limit: int = 5):
    places_db = [
        {"name": "Eiffel Tower", "city": "Paris", "tags": ["history", "architecture"]},
        {"name": "Acropolis", "city": "Athens", "tags": ["history", "culture"]},
        {"name": "Bondi Beach", "city": "Sydney", "tags": ["beach", "surfing"]},
        {"name": "Statue of Liberty", "city": "New York", "tags": ["history", "monument"]},
        {"name": "Mount Fuji", "city": "Tokyo", "tags": ["nature", "mountain"]},
    ]

    # фильтрация по интересам
    filtered = [p for p in places_db if any(tag in p["tags"] for tag in interests)]

    return filtered[:limit]

