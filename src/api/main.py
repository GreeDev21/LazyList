import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env antes de importar módulos que las necesiten
load_dotenv()

# Configurar el sistema de logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("lazylist")
logger.info("Sistema de logs de LazyList inicializado con éxito.")

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any

from src.application.use_cases import ContentManager
from src.infrastructure.database import Database
from src.infrastructure.sqlite_repository import (
    SQLitePeliculaRepository, SQLiteSerieRepository, SQLiteAnimeRepository, 
    SQLiteMangaRepository, SQLiteComicRepository, SQLiteNovelaRepository,
    SQLiteLibroRepository, SQLiteRecursoRepository, SQLiteJuegoRepository
)

# Idealmente este setup estaría en un contenedor DI (Dependency Injection), 
# pero para FastAPI usamos la inyección por dependencias nativa.
db = Database()
db.init_db()

from src.infrastructure.api_clients.router_client import RouterApiClient

# Inicializar repositorios reales
repos = {
    "peliculas": SQLitePeliculaRepository(db),
    "series": SQLiteSerieRepository(db),
    "series_tvmaze": SQLiteSerieRepository(db), # Comparten repositorio
    "anime": SQLiteAnimeRepository(db),
    "mangas": SQLiteMangaRepository(db),
    "comics": SQLiteComicRepository(db),
    "novelas": SQLiteNovelaRepository(db),
    "libros": SQLiteLibroRepository(db),
    "recursos": SQLiteRecursoRepository(db),
    "juegos": SQLiteJuegoRepository(db)
}

# Inicializar el enrutador maestro de APIs
api_router = RouterApiClient()

content_manager = ContentManager(api_client=api_router, repos=repos)

def get_content_manager() -> ContentManager:
    return content_manager

app = FastAPI(title="LazyList API")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod debería ser restringido
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend estático (vanilla + Tailwind, servido por FastAPI)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse("static/index.html")

from typing import Optional

class SaveRequest(BaseModel):
    api_id: str
    category: str

class ManualItemRequest(BaseModel):
    category: str
    titulo: str
    estado: str

@app.post("/api/items/manual")
def create_manual_item(req: ManualItemRequest):
    try:
        repo = repos.get(req.category)
        if not repo:
            raise HTTPException(status_code=400, detail="Categoría inválida")
        
        import uuid
        item_id = f"manual_{uuid.uuid4().hex[:8]}"
        
        import inspect
        entity_class = inspect.signature(repo.save).parameters['item'].annotation
        
        item = entity_class(
            id=item_id,
            titulo=req.titulo,
            estado=req.estado
        )
        repo.save(item)
        
        r_dict = item.model_dump()
        r_dict["category"] = req.category
        return r_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class UpdateRequest(BaseModel):
    estado: Optional[str] = None
    notas: Optional[str] = None
    calificacion: Optional[float] = None

@app.get("/api/items")
def get_all_items():
    try:
        from sqlmodel import select
        from src.domain.entities import (Pelicula, Serie, Anime, Manga, Comic, Novela, Libro, Juego, Recurso)
        items = []
        with db.get_session() as session:
            for entity_class, category_name in [
                (Pelicula, "peliculas"), (Serie, "series"), (Anime, "anime"),
                (Manga, "mangas"), (Comic, "comics"), (Novela, "novelas"),
                (Libro, "libros"), (Juego, "juegos"), (Recurso, "recursos")
            ]:
                records = session.exec(select(entity_class)).all()
                for r in records:
                    r_dict = r.model_dump()
                    r_dict["category"] = category_name
                    items.append(r_dict)
            return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/items/{category}/{item_id}")
def update_item(category: str, item_id: str, req: UpdateRequest):
    try:
        repo = repos.get(category)
        if not repo:
            raise HTTPException(status_code=400, detail=f"No hay repositorio para la categoría {category}")
        
        # repo.get_by_id creates a new session and detached object, so we must merge it when saving.
        item = repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item no encontrado")
            
        if req.estado is not None:
            item.estado = req.estado
        if req.notas is not None:
            item.notas = req.notas
        if req.calificacion is not None:
            item.calificacion = req.calificacion
                
        repo.save(item)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/items/{category}/{item_id}")
def delete_item(category: str, item_id: str):
    try:
        repo = repos.get(category)
        if not repo:
            raise HTTPException(status_code=400, detail=f"No hay repositorio para la categoría {category}")
            
        with db.get_session() as session:
            # We get the underlying entity class from the repository type hint
            import inspect
            entity_class = inspect.signature(repo.save).parameters['item'].annotation
            item = session.get(entity_class, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            
            session.delete(item)
            session.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search", response_model=List[Dict[str, Any]])
def search_items(q: str, category: str, manager: ContentManager = Depends(get_content_manager)):
    """Busca items en la API externa configurada para la categoría."""
    try:
        return manager.search_external(q, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save")
def save_item(req: SaveRequest, manager: ContentManager = Depends(get_content_manager)):
    """Guarda un item obteniendo sus detalles completos desde la API externa."""
    try:
        saved_entity = manager.save_from_api(req.api_id, req.category)
        return saved_entity.model_dump()
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/generos")
def get_generos():
    """Devuelve la lista maestra de géneros disponibles."""
    try:
        from sqlmodel import select
        from src.domain.entities import Genero
        with db.get_session() as session:
            generos = session.exec(select(Genero)).all()
            return [{"id": g.id, "nombre": g.nombre} for g in generos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
