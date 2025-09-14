from fastapi.testclient import TestClient
from destination_service.main import app

client = TestClient(app)

def test_get_destinations_history():
    resp = client.get("/destinations", params=[("interests", "history"), ("limit", 2)])
    assert resp.status_code == 200
    data = resp.json()
    assert "destinations" in data
    assert isinstance(data["destinations"], list)
