import pytest
from src.infrastructure.api_clients.mangadex_client import MangaDexClient

from dotenv import load_dotenv

@pytest.fixture
def mangadex_client():
    load_dotenv()
    return MangaDexClient()

def test_search_manga(mangadex_client):
    results = mangadex_client.search("Berserk", "mangas")
    assert len(results) > 0
    first = results[0]
    assert "api_id" in first
    assert "title" in first

def test_get_manga_details(mangadex_client):
    # ID de Berserk en MangaDex: 801513ba-a712-498c-8f57-cae55b38cc92
    details = mangadex_client.get_details("801513ba-a712-498c-8f57-cae55b38cc92", "mangas")
    
    assert details["title_romaji"] == "Berserk" or "Berserk" in details["title_romaji"]
    assert details["autor"] == "Miura Kentarou" # MangaDex usually formats it this way
    assert details["status"] in ["ongoing", "completed", "hiatus", "cancelled"]
    assert details["year"] == 1989
