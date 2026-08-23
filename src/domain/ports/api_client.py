from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ApiClientPort(ABC):
    """
    Puerto (Interfaz) para interactuar con APIs externas (TMDB, AniList, etc.).
    Aisla la lógica de negocio de los detalles HTTP.
    """
    
    @abstractmethod
    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        """
        Realiza una búsqueda ligera (Paso 1).
        Devuelve una lista de diccionarios con información básica (ID, Título, Año).
        """
        pass
        
    @abstractmethod
    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        """
        Obtiene los detalles completos de un ítem por su ID de API (Paso 2).
        Devuelve un diccionario listo para ser mapeado a una Entidad de Dominio.
        """
        pass
