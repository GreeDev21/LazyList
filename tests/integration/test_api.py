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

def test_bulk_creation_endpoint():
    import uuid
    suffix = uuid.uuid4().hex[:6]
    title_a = f"Pelicula Lote A {suffix}"
    title_b = f"Pelicula Lote B {suffix}"
    title_c = f"Pelicula Lote C {suffix}"
    title_j = f"Juego Lote A {suffix}"

    # Test con peliculas (no tiene columna estado en la entidad, se ignora al guardar)
    response = client.post("/api/items/bulk", json={
        "category": "peliculas",
        "estado": "pendiente",
        "items": [title_a, title_b]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == title_a
    assert data[0]["id"].startswith("manual_")
    assert data[1]["title"] == title_b
    assert data[1]["id"].startswith("manual_")

    # Test con duplicados (debe saltarse title_a porque ya se creó arriba)
    response_dup = client.post("/api/items/bulk", json={
        "category": "peliculas",
        "estado": "pendiente",
        "items": [title_a, title_c]
    })
    assert response_dup.status_code == 200
    data_dup = response_dup.json()
    assert len(data_dup) == 1
    assert data_dup[0]["title"] == title_c

    # Test con juegos (sí tiene columna estado en la entidad, se persiste)
    response_juego = client.post("/api/items/bulk", json={
        "category": "juegos",
        "estado": "en_curso",
        "items": [title_j]
    })
    assert response_juego.status_code == 200
    data_juego = response_juego.json()
    assert len(data_juego) == 1
    assert data_juego[0]["titulo"] == title_j
    assert data_juego[0]["estado"] == "en_curso"
    assert data_juego[0]["id"].startswith("manual_")
