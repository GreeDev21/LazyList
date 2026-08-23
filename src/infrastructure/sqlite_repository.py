from typing import List, Optional
from src.domain.entities import Pelicula, Serie, Anime, Manga, Comic, Novela, Libro, Juego, Recurso, Genero
from src.domain.ports.repository import RepositoryPort
from src.infrastructure.database import Database
from sqlmodel import select

class SQLitePeliculaRepository(RepositoryPort[Pelicula]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Pelicula) -> Pelicula:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Pelicula]:
        with self.db.get_session() as session:
            return session.get(Pelicula, item_id)
    def get_all(self) -> List[Pelicula]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteSerieRepository(RepositoryPort[Serie]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Serie) -> Serie:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Serie]:
        with self.db.get_session() as session:
            return session.get(Serie, item_id)
    def get_all(self) -> List[Serie]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteAnimeRepository(RepositoryPort[Anime]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Anime) -> Anime:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Anime]:
        with self.db.get_session() as session:
            return session.get(Anime, item_id)
    def get_all(self) -> List[Anime]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteMangaRepository(RepositoryPort[Manga]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Manga) -> Manga:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Manga]:
        with self.db.get_session() as session:
            return session.get(Manga, item_id)
    def get_all(self) -> List[Manga]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteComicRepository(RepositoryPort[Comic]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Comic) -> Comic:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Comic]:
        with self.db.get_session() as session:
            return session.get(Comic, item_id)
    def get_all(self) -> List[Comic]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteNovelaRepository(RepositoryPort[Novela]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Novela) -> Novela:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Novela]:
        with self.db.get_session() as session:
            return session.get(Novela, item_id)
    def get_all(self) -> List[Novela]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteLibroRepository(RepositoryPort[Libro]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Libro) -> Libro:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Libro]:
        with self.db.get_session() as session:
            return session.get(Libro, item_id)
    def get_all(self) -> List[Libro]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteRecursoRepository(RepositoryPort[Recurso]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Recurso) -> Recurso:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Recurso]:
        with self.db.get_session() as session:
            return session.get(Recurso, item_id)
    def get_all(self) -> List[Recurso]: pass
    def delete(self, item_id: str) -> bool: pass

class SQLiteJuegoRepository(RepositoryPort[Juego]):
    def __init__(self, db: Database): self.db = db
    def save(self, item: Juego) -> Juego:
        with self.db.get_session() as session:
            item = session.merge(item)
            session.commit()
            return item
    def get_by_id(self, item_id: str) -> Optional[Juego]:
        with self.db.get_session() as session:
            return session.get(Juego, item_id)
    def get_all(self) -> List[Juego]: pass
    def delete(self, item_id: str) -> bool: pass
