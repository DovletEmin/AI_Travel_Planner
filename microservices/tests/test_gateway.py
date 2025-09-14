import pytest
import respx
from fastapi.testclient import TestClient
from gateway_service.main import app
import httpx

client = TestClient(app)

@respx.mock
def test_plan_trip_gateway():
    respx.get("http://127.0.0.1:8001/destinations").mock(
        return_value=httpx.Response(
            200,
            json={
                "destinations": [
                    {"name": "Eiffel Tower", "city": "Paris"},
                    {"name": "Bondi Beach", "city": "Sydney"},
                ]
            }
        )
    )

    respx.get("http://127.0.0.1:8002/weather").mock(
        return_value=httpx.Response(
            200,
            json={"temperature": 25, "description": "clear sky"}
        )
    )

    respx.get("http://127.0.0.1:8003/hotels").mock(
        return_value=httpx.Response(
            200,
            json={
                "hotels": [
                    {"name": "Hotel Paris 1", "city": "Paris"},
                    {"name": "Hotel Paris 2", "city": "Paris"},
                    {"name": "Hotel Sydney 1", "city": "Sydney"},
                    {"name": "Hotel Sydney 2", "city": "Sydney"},
                ]
            }
        )
    )

    payload = {
        "interests": ["history", "beach"],
        "limit": 2,
        "min_temp": 20,
        "max_temp": 30,
        "weather_contains": "clear"
    }

    response = client.post("/plan", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "plan" in data
    assert len(data["plan"]) == 2

    for place in data["plan"]:
        assert "name" in place
        assert "city" in place
        assert "weather" in place
