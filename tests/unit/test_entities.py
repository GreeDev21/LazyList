import pytest
from pydantic import ValidationError
from src.domain.entities import (
    Pelicula, Serie, Anime, Manga, Comic, Novela, Libro, Recurso, Juego, Genero
)

def test_pelicula_creation():
    p = Pelicula(title="The Batman", original_title="The Batman", genre=["Action"], release_date="2022-03-01", director="Matt Reeves", duracion=176, origin_country=["US"])
    assert p.title == "The Batman"

def test_pelicula_requires_title():
    with pytest.raises(ValidationError):
        Pelicula.model_validate({"director": "Falta el titulo"})

def test_serie_creation():
    s = Serie(title="Breaking Bad", original_title="Breaking Bad", genre=["Drama"], origin_country=["US"], status="Ended", premiered="2008-01-20", ended="2013-09-29", plataform="AMC")
    assert s.title == "Breaking Bad"

def test_anime_creation():
    a = Anime(title_english="Shield Hero", title_romaji="Tate no Yuusha", episodios=25, status="FINISHED", genre=["Action"], premiered="2019-01-09", ended="2019-06-26")
    assert a.title_english == "Shield Hero"

def test_manga_creation():
    m = Manga(title_english="Berserk", title_romaji="Berserk", status="ongoing", year=1989, autor="Kentaro Miura", capitulos=376)
    assert m.autor == "Kentaro Miura"

def test_comic_creation():
    c = Comic(title="Absolute Batman", year=2024, publisher="DC", capitulos=15, genero=["Superhero"], escritor="Scott Snyder", status="Ongoing")
    assert c.publisher == "DC"

def test_novela_creation():
    n = Novela(title="Solo Leveling", year=2016, capitulos=270, genero=["Action"], escritor="Chugong", status="Completed")
    assert n.escritor == "Chugong"

def test_libro_creation():
    l = Libro(titulo="Soft Skills", autor="John Sonmez", ano=2014, genero=["Self-help"], saga="", orden=0)
    assert l.titulo == "Soft Skills"

def test_recurso_creation():
    r = Recurso(titulo="FastAPI Tutorial", url="https://youtube.com/...", creado_autor="Codigofacilito", volver_a_ver=True, notas="Muy bueno", tipo="Video", NSFW=False)
    assert r.url.startswith("http")

def test_juego_creation():
    j = Juego(titulo="The Witcher 3", mod="", tienda="Steam", estado="Jugando")
    assert j.tienda == "Steam"

def test_genero_creation():
    g = Genero(id="28", nombre="Acción")
    assert g.nombre == "Acción"
