import pytest
from fastapi.testclient import TestClient
from src.api.main import app, get_content_manager
from src.application.use_cases import ContentManager
from tests.unit.test_use_cases import MockApiClient, MockRepository

# Inyección de dependencias para Testing (Mocks)
def override_get_content_manager():
    repo = MockRepository()
    api = MockApiClient()
    return ContentManager(api_client=api, repos={"peliculas": repo})

app.dependency_overrides[get_content_manager] = override_get_content_manager

client = TestClient(app)

def test_search_endpoint():
    response = client.get("/api/search?q=The Batman&category=peliculas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "The Batman"

def test_save_from_api_endpoint():
    response = client.post("/api/save", json={"api_id": "tt123", "category": "peliculas"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Batman"
    assert data["duracion"] == 176
