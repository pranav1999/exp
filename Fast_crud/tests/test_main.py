from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
    assert response.json()["description"] == "This is a test item."

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
