from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

# Definimos una variable de tipo genérico para que el repositorio 
# sirva para cualquier entidad (Pelicula, Juego, Libro, etc.)
T = TypeVar("T")

class RepositoryPort(ABC, Generic[T]):
    """
    Puerto (Interfaz) del Repositorio.
    El Dominio exige que CUALQUIER base de datos que usemos en el futuro
    (SQLite, Postgres, MongoDB) DEBE cumplir con este contrato.
    """
    
    @abstractmethod
    def save(self, item: T) -> T:
        """Guarda o actualiza un ítem en la base de datos."""
        pass
        
    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[T]:
        """Busca un ítem por su ID único."""
        pass
        
    @abstractmethod
    def get_all(self) -> List[T]:
        """Devuelve todos los ítems de este tipo."""
        pass
        
    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Elimina un ítem por su ID. Retorna True si se eliminó, False si no existía."""
        pass
