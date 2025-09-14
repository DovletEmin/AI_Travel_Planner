import pytest
from fastapi.testclient import TestClient
from hotel_service.main import app

client = TestClient(app)

def test_get_hotels_for_city():
    response = client.get("/hotels", params={"city": "Paris"})
    assert response.status_code == 200
    data = response.json()
    assert "hotels" in data
    assert len(data["hotels"]) == 2