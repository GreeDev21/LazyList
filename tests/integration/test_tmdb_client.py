import pytest
from src.infrastructure.api_clients.tmdb_client import TMDBClient

from dotenv import load_dotenv

@pytest.fixture
def tmdb_client():
    load_dotenv()
    return TMDBClient()

def test_search_movie(tmdb_client):
    results = tmdb_client.search("The Batman", "peliculas")
    assert len(results) > 0
    # Comprobamos que trajo la estructura ligera de paso 1
    first = results[0]
    assert "api_id" in first
    assert "title" in first
    assert "year" in first
    assert "overview" in first

def test_get_movie_details(tmdb_client):
    # ID de The Batman (2022) = 414906
    details = tmdb_client.get_details("414906", "peliculas")
    
    assert details["title"] == "The Batman"
    assert details["director"] == "Matt Reeves"
    assert details["duracion"] >= 170
    assert "US" in details["origin_country"]
    assert "Acción" in details["genre"] or "Action" in details["genre"] or len(details["genre"]) > 0

def test_unsupported_category(tmdb_client):
    with pytest.raises(NotImplementedError):
        tmdb_client.search("Naruto", "anime")
