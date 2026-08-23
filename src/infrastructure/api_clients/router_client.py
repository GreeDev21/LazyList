from typing import List, Dict, Any, Optional
from src.domain.ports.api_client import ApiClientPort
from src.infrastructure.api_clients.tmdb_client import TMDBClient
from src.infrastructure.api_clients.anilist_client import AniListClient
from src.infrastructure.api_clients.mangadex_client import MangaDexClient
from src.infrastructure.api_clients.comicvine_client import ComicVineClient
from src.infrastructure.api_clients.tvmaze_client import TvMazeClient
from src.infrastructure.api_clients.googlebooks_client import GoogleBooksClient
from src.infrastructure.api_clients.igdb_client import IGDBClient
from src.infrastructure.api_clients.generic_scraper_client import UrlScraperClient
from src.infrastructure.api_clients.youtube_client import YouTubeApiClient

import logging

logger = logging.getLogger("lazylist")

class RouterApiClient(ApiClientPort):
    """
    Enrutador central que delega la petición al cliente API correcto
    según la categoría solicitada.
    """
    def __init__(self):
        self.tmdb = TMDBClient()
        self.anilist = AniListClient()
        self.mangadex = MangaDexClient()
        self.comicvine = ComicVineClient()
        self.tvmaze = TvMazeClient()
        self.googlebooks = GoogleBooksClient()
        self.igdb = IGDBClient()
        self.scraper = UrlScraperClient()
        self.youtube = YouTubeApiClient()

    def _get_client_for_category(self, category: str, query_or_id: Optional[str] = None) -> ApiClientPort:
        if category in ["peliculas", "series"]:
            return self.tmdb
        elif category == "series_tvmaze":
            return self.tvmaze
        elif category in ["anime"]:
            return self.anilist
        elif category in ["mangas"]:
            return self.mangadex
        elif category in ["comics"]:
            return self.comicvine
        elif category in ["libros", "novelas"]:
            return self.googlebooks
        elif category in ["juegos"]:
            return self.igdb
        elif category in ["recursos"]:
            if query_or_id and self.youtube.extract_video_id(query_or_id):
                return self.youtube
            return self.scraper
        else:
            raise NotImplementedError(f"No hay un cliente API configurado para la categoría: {category}")

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        logger.info(f"Iniciando búsqueda externa: query='{query}', categoria='{category}'")
        client = self._get_client_for_category(category, query)
        try:
            results = client.search(query, category)
            logger.info(f"Búsqueda externa completada con éxito. Resultados: {len(results)}")
            return results
        except Exception as e:
            logger.error(f"Error en la búsqueda externa para la categoría '{category}' con query '{query}': {str(e)}", exc_info=True)
            raise

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        logger.info(f"Obteniendo detalles externos: api_id='{api_id}', categoria='{category}'")
        client = self._get_client_for_category(category, api_id)
        try:
            details = client.get_details(api_id, category)
            logger.info(f"Detalles obtenidos con éxito para api_id='{api_id}'")
            return details
        except Exception as e:
            logger.error(f"Error al obtener detalles externos para la categoría '{category}' con api_id '{api_id}': {str(e)}", exc_info=True)
            raise


