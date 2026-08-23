from typing import Dict, Any, List
from src.domain.ports.repository import RepositoryPort
from src.domain.ports.api_client import ApiClientPort
from src.domain.entities import Pelicula, Serie, Anime, Manga, Comic, Novela, Libro, Juego, Recurso

class ContentManager:
    """
    Capa de Aplicación (Casos de Uso).
    Orquesta la comunicación entre los puertos (APIs y Repositorios)
    sin conocer detalles de su implementación (SQLite, TMDB, etc.).
    """
    def __init__(self, api_client: ApiClientPort, repos: Dict[str, RepositoryPort]):
        self.api_client = api_client
        self.repos = repos
        
        # Mapa de factorías (Factory registry) para seguir principios SOLID (OCP)
        self.entity_factories = {
            "peliculas": Pelicula,
            "series": Serie,
            "series_tvmaze": Serie,
            "anime": Anime,
            "mangas": Manga,
            "comics": Comic,
            "libros": Libro,
            "recursos": Recurso,
            "juegos": Juego,
            "novelas": Novela,
        }

    def search_external(self, query: str, category: str) -> List[Dict[str, Any]]:
        """
        Paso 1: Búsqueda Interactiva.
        Busca en la API externa y devuelve una lista de coincidencias ligeras.
        """
        return self.api_client.search(query, category)

    def save_from_api(self, api_id: str, category: str) -> Any:
        """
        Paso 2: Fetch Detallado y Guardado.
        Obtiene los detalles completos de la API externa por ID,
        lo convierte a una entidad de dominio y lo guarda.
        """
        raw_data = self.api_client.get_details(api_id, category)
        
        # Mapeamos los datos crudos a nuestra Entidad usando el registro
        factory = self.entity_factories.get(category)
        if not factory:
            raise NotImplementedError(f"Categoría {category} no soportada aún para guardado automático")
            
        if "estado" not in raw_data:
            raw_data["estado"] = "pendiente"
            
        item = factory(**raw_data)
            
        repo = self.repos.get(category)
        if not repo:
            raise ValueError(f"No hay repositorio inyectado para la categoría {category}")
            
        return repo.save(item)
