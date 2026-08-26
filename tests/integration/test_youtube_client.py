import os
import pytest
from dotenv import load_dotenv
from src.infrastructure.api_clients.youtube_client import YouTubeApiClient

@pytest.fixture
def youtube_client():
    load_dotenv()
    # Saltar la prueba si la API KEY no está configurada
    if not os.getenv("YOUTUBE_API_KEY"):
        pytest.skip("YOUTUBE_API_KEY no configurado en el archivo .env")
    return YouTubeApiClient()

def test_extract_video_id(youtube_client):
    # Test con diferentes variantes de URLs válidas de YouTube
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://youtube.com/shorts/dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
    for url in urls:
        assert youtube_client.extract_video_id(url) == "dQw4w9WgXcQ"

    # Test con URLs inválidas
    assert youtube_client.extract_video_id("https://google.com") == ""
    assert youtube_client.extract_video_id("") == ""

def test_search_youtube_video(youtube_client):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    results = youtube_client.search(url, "recursos")
    
    assert len(results) == 1
    assert results[0]["api_id"] == url
    assert "Never Gonna Give You Up" in results[0]["title"]
    assert "Rick" in results[0]["overview"] or "Astley" in results[0]["overview"] or len(results[0]["overview"]) > 0

def test_get_youtube_details(youtube_client):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    details = youtube_client.get_details(url, "recursos")
    
    assert details["id"] == "yt_dQw4w9WgXcQ"
    assert "Never Gonna Give You Up" in details["titulo"]
    assert details["url"] == url
    assert details["creado_autor"] == "Rick Astley"
    assert details["tipo"] == "Video"

def test_unsupported_category(youtube_client):
    with pytest.raises(NotImplementedError):
        youtube_client.search("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "peliculas")
