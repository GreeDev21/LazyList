import pytest
import sqlite3
import os
from src.domain.entities import Pelicula, Comic
from src.infrastructure.database import Database
from src.infrastructure.sqlite_repository import SQLitePeliculaRepository, SQLiteComicRepository

@pytest.fixture
def db():
    # Usamos una base de datos en memoria para los tests aislando el entorno real
    database = Database(":memory:")
    database.init_db()
    return database

def test_guardar_y_obtener_pelicula(db):
    repo = SQLitePeliculaRepository(db)
    peli = Pelicula(
        id="tt123",
        title="The Batman",
        original_title="The Batman",
        release_date="2022-03-01",
        director="Matt Reeves",
        duracion=176,
        origin_country=["US"]
    )
    
    repo.save(peli)
    
    # Recuperamos
    saved = repo.get_by_id("tt123")
    assert saved is not None
    assert saved.title == "The Batman"
    assert saved.director == "Matt Reeves"
    assert saved.origin_country == ["US"]
    
def test_guardar_y_obtener_comic(db):
    repo = SQLiteComicRepository(db)
    comic = Comic(
        id="cv456",
        title="Absolute Batman",
        year=2024,
        publisher="DC",
        capitulos=15,
        escritor="Scott Snyder",
        status="Ongoing"
    )
    
    repo.save(comic)
    
    saved = repo.get_by_id("cv456")
    assert saved is not None
    assert saved.title == "Absolute Batman"
    assert saved.publisher == "DC"
