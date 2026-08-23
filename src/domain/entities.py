from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class Genero(SQLModel, table=True):
    __tablename__ = "generos"
    id: str = Field(primary_key=True)
    nombre: str

class Pelicula(SQLModel, table=True):
    __tablename__ = "peliculas"
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    original_title: Optional[str] = None
    genre: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    release_date: Optional[str] = None
    director: Optional[str] = None
    duracion: Optional[int] = None
    origin_country: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    notas: Optional[str] = None
    calificacion: Optional[int] = None
    
class Serie(SQLModel, table=True):
    __tablename__ = "series"
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    original_title: Optional[str] = None
    genre: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    origin_country: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    status: Optional[str] = None
    premiered: Optional[str] = None
    ended: Optional[str] = None
    plataform: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Anime(SQLModel, table=True):
    __tablename__ = "anime"
    id: Optional[str] = Field(default=None, primary_key=True)
    title_english: Optional[str] = None
    title_romaji: str
    episodios: Optional[int] = None
    status: Optional[str] = None
    genre: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    premiered: Optional[str] = None
    ended: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Manga(SQLModel, table=True):
    __tablename__ = "mangas"
    id: Optional[str] = Field(default=None, primary_key=True)
    title_english: Optional[str] = None
    title_romaji: str
    status: Optional[str] = None
    year: Optional[int] = None
    autor: Optional[str] = None
    capitulos: Optional[int] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Comic(SQLModel, table=True):
    __tablename__ = "comics"
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    year: Optional[int] = None
    publisher: Optional[str] = None
    capitulos: Optional[int] = None
    escritor: Optional[str] = None
    status: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Novela(SQLModel, table=True):
    __tablename__ = "novelas"
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    year: Optional[int] = None
    capitulos: Optional[int] = None
    genero: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    escritor: Optional[str] = None
    status: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Libro(SQLModel, table=True):
    __tablename__ = "libros"
    id: Optional[str] = Field(default=None, primary_key=True)
    titulo: str
    autor: Optional[str] = None
    ano: Optional[int] = None
    genero: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    saga: Optional[str] = None
    orden: Optional[int] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None

class Recurso(SQLModel, table=True):
    __tablename__ = "recursos"
    id: Optional[str] = Field(default=None, primary_key=True)
    titulo: str
    url: str
    creado_autor: Optional[str] = None
    volver_a_ver: Optional[bool] = None
    notas: Optional[str] = None
    tipo: Optional[str] = None
    NSFW: Optional[bool] = False
    calificacion: Optional[int] = None

class Juego(SQLModel, table=True):
    __tablename__ = "juegos"
    id: Optional[str] = Field(default=None, primary_key=True)
    titulo: str
    mod: Optional[str] = None
    tienda: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[int] = None
