import pytest
from fastapi.testclient import TestClient
from weather_service.main import app

client = TestClient(app)

def test_get_weather_valid_city():
    response = client.get("/weather", params={"city": "Paris"})
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "description" in data