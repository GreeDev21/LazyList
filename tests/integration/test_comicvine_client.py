import pytest
from src.infrastructure.api_clients.comicvine_client import ComicVineClient
from dotenv import load_dotenv

@pytest.fixture
def comicvine_client():
    load_dotenv()
    return ComicVineClient()

def test_search_comic(comicvine_client):
    results = comicvine_client.search("Absolute Batman", "comics")
    assert len(results) > 0
    first = results[0]
    assert "api_id" in first
    assert "title" in first
    assert "year" in first

def test_get_comic_details(comicvine_client):
    # ID de Absolute Batman (2024) en ComicVine: 161817 (ejemplo asumiendo un ID)
    # Hacemos una búsqueda para obtener un ID válido dinámicamente
    results = comicvine_client.search("Absolute Batman", "comics")
    valid_id = results[0]["api_id"]
    
    details = comicvine_client.get_details(valid_id, "comics")
    
    assert "Batman" in details["title"]
    assert details["publisher"] is not None
