import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_hotels():
    response = client.post("/api/hotels", json={
        "checkIn": "2024-09-22",
        "checkOut": "2024-09-23",
        "rooms": 1,
        "adults": 2,
        "children": 2,
        "cityId": 78471
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Add more specific assertions based on your expected response structure

# Add more tests as needed