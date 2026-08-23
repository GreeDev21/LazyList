import pytest
from src.infrastructure.api_clients.anilist_client import AniListClient

@pytest.fixture
def anilist_client():
    return AniListClient()

def test_search_anime(anilist_client):
    results = anilist_client.search("Frieren", "anime")
    assert len(results) > 0
    first = results[0]
    assert "api_id" in first
    assert "title" in first
    assert "year" in first
    
def test_search_manga(anilist_client):
    results = anilist_client.search("Berserk", "mangas")
    assert len(results) > 0
    first = results[0]
    assert "api_id" in first
    assert "title" in first
    
def test_get_anime_details(anilist_client):
    # ID de Sousou no Frieren en AniList: 154587
    details = anilist_client.get_details("154587", "anime")
    
    assert "Frieren" in details["title_romaji"]
    assert details["episodios"] == 28
    assert details["status"] == "FINISHED"
    assert "Adventure" in details["genre"]
    assert details["premiered"].startswith("2023")

def test_get_manga_details(anilist_client):
    # ID de Berserk en AniList: 30002
    details = anilist_client.get_details("30002", "mangas")
    
    assert "Berserk" in details["title_romaji"]
    assert "Action" in details["genre"]
