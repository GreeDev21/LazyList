import pytest
from src.domain.entities import Pelicula
from src.domain.ports.repository import RepositoryPort
from src.domain.ports.api_client import ApiClientPort
from src.application.use_cases import ContentManager

# Mocks para TDD
class MockRepository(RepositoryPort[Pelicula]):
    def __init__(self):
        self.db = {}
        
    def save(self, item: Pelicula) -> Pelicula:
        self.db[item.id] = item
        return item
        
    def get_by_id(self, item_id: str) -> Pelicula | None:
        return self.db.get(item_id)
        
    def get_all(self):
        return list(self.db.values())
        
    def delete(self, item_id: str) -> bool:
        if item_id in self.db:
            del self.db[item_id]
            return True
        return False

class MockApiClient(ApiClientPort):
    def search(self, query: str, category: str):
        if query == "The Batman":
            return [{"api_id": "tt123", "title": "The Batman", "year": "2022"}]
        return []
        
    def get_details(self, api_id: str, category: str):
        if api_id == "tt123":
            return {
                "id": "tt123",
                "title": "The Batman",
                "original_title": "The Batman",
                "release_date": "2022-03-01",
                "director": "Matt Reeves",
                "duracion": 176,
                "origin_country": ["US"]
            }
        return {}

def test_interactive_search():
    api = MockApiClient()
    manager = ContentManager(api_client=api, repos={})
    
    results = manager.search_external("The Batman", "peliculas")
    
    assert len(results) == 1
    assert results[0]["title"] == "The Batman"

def test_save_from_api_details():
    repo = MockRepository()
    api = MockApiClient()
    manager = ContentManager(api_client=api, repos={"peliculas": repo})
    
    # Simulamos el paso 2: el usuario hace clic en el ID tt123
    saved_item = manager.save_from_api("tt123", "peliculas")
    
    assert saved_item is not None
    assert saved_item.id == "tt123"
    assert saved_item.director == "Matt Reeves"
    
    # Verificamos que se guardó en el repo
    in_db = repo.get_by_id("tt123")
    assert in_db.duracion == 176
