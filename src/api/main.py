import os
import logging
from dotenv import load_dotenv
from src.config.paths import STATIC_DIR, ENV_PATH, LOG_PATH

# Cargar variables de entorno desde el archivo .env antes de importar módulos que las necesiten
load_dotenv(dotenv_path=ENV_PATH)

# Configurar el sistema de logging global tanto a consola como a archivo lazylist.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8", mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lazylist")
logger.info(f"Sistema de logs de LazyList inicializado con éxito. Archivo de log: {LOG_PATH}")

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
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

from typing import Optional

class SaveRequest(BaseModel):
    api_id: str
    category: str

class ManualItemRequest(BaseModel):
    category: str
    titulo: str
    estado: str
    fields: Optional[dict] = None

@app.post("/api/items/manual")
def create_manual_item(req: ManualItemRequest):
    logger.info(f"POST /api/items/manual: categoria='{req.category}', titulo='{req.titulo}'")
    try:
        repo = repos.get(req.category)
        if not repo:
            raise HTTPException(status_code=400, detail="Categoría inválida")
        
        import uuid
        item_id = f"manual_{uuid.uuid4().hex[:8]}"
        
        import inspect
        entity_class = inspect.signature(repo.save).parameters['item'].annotation
        
        kwargs = {"id": item_id}
        if hasattr(entity_class, 'estado'):
            kwargs['estado'] = req.estado
        
        if hasattr(entity_class, 'title'):
            kwargs['title'] = req.titulo
        elif hasattr(entity_class, 'title_romaji'):
            kwargs['title_romaji'] = req.titulo
        elif hasattr(entity_class, 'titulo'):
            kwargs['titulo'] = req.titulo
            
        if req.fields:
            for k, v in req.fields.items():
                if hasattr(entity_class, k):
                    kwargs[k] = v
                    
        item = entity_class(**kwargs)
        repo.save(item)
        logger.info(f"Item manual creado exitosamente: id='{item_id}', categoria='{req.category}'")
        
        r_dict = item.model_dump()
        r_dict["category"] = req.category
        return r_dict
    except Exception as e:
        logger.error(f"Error al crear item manual ({req.category}): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

class BulkItemRequest(BaseModel):
    category: str
    estado: str
    items: List[str]

class EnrichRequest(BaseModel):
    category: str
    id: str
    api_id: str

@app.post("/api/items/bulk")
def create_bulk_items(req: BulkItemRequest):
    logger.info(f"POST /api/items/bulk: categoria='{req.category}', items_count={len(req.items)}, estado='{req.estado}'")
    try:
        repo = repos.get(req.category)
        if not repo:
            raise HTTPException(status_code=400, detail="Categoría inválida")
        
        import inspect
        entity_class = inspect.signature(repo.save).parameters['item'].annotation
        
        created_items = []
        import uuid
        
        with db.get_session() as session:
            from sqlalchemy import func
            from sqlmodel import select
            
            # Obtener el atributo correspondiente al título para comprobación de repetidos
            title_attr = None
            if hasattr(entity_class, 'title'):
                title_attr = entity_class.title
            elif hasattr(entity_class, 'title_romaji'):
                title_attr = entity_class.title_romaji
            elif hasattr(entity_class, 'titulo'):
                title_attr = entity_class.titulo
                
            for title in req.items:
                # Comprobar duplicado en la base de datos (case-insensitive)
                existing = None
                if req.category == "recursos":
                    existing = session.exec(select(entity_class).where(func.lower(entity_class.url) == title.lower())).first()
                elif title_attr is not None:
                    existing = session.exec(select(entity_class).where(func.lower(title_attr) == title.lower())).first()
                    
                if existing is not None:
                    continue  # Si ya existe, saltear para evitar duplicados
                
                item_id = f"manual_{uuid.uuid4().hex[:8]}"
                kwargs = {"id": item_id}
                if hasattr(entity_class, 'estado'):
                    kwargs['estado'] = req.estado
                
                if hasattr(entity_class, 'title'):
                    kwargs['title'] = title
                elif hasattr(entity_class, 'title_romaji'):
                    kwargs['title_romaji'] = title
                elif hasattr(entity_class, 'titulo'):
                    kwargs['titulo'] = title
                    
                if hasattr(entity_class, 'url'):
                    kwargs['url'] = title
                    
                item = entity_class(**kwargs)
                session.merge(item)
                
                r_dict = item.model_dump()
                r_dict["category"] = req.category
                created_items.append(r_dict)
                
            session.commit()
            logger.info(f"Carga por lote completada con éxito. Creados: {len(created_items)} ítems en categoría '{req.category}'.")
            
        return created_items
    except Exception as e:
        logger.error(f"Error en carga por lote para categoría '{req.category}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/items/enrich")
def enrich_manual_item(req: EnrichRequest):
    try:
        repo = repos.get(req.category)
        if not repo:
            raise HTTPException(status_code=400, detail="Categoría inválida")
            
        raw_data = api_router.get_details(req.api_id, req.category)
        
        item = repo.get_by_id(req.id)
        if not item:
            raise HTTPException(status_code=404, detail="Elemento no encontrado")
            
        for k, v in raw_data.items():
            if k in ["id", "notas", "calificacion", "estado"]:
                continue
            if hasattr(item, k):
                setattr(item, k, v)
                
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
    volver_a_ver: Optional[bool] = None

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
        if req.volver_a_ver is not None and hasattr(item, 'volver_a_ver'):
            item.volver_a_ver = req.volver_a_ver
                
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
