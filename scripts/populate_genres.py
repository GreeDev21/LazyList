import os
import sys
import httpx
from dotenv import load_dotenv

# Asegurar que los imports relativos funcionen desde la raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.database import Database
from src.domain.entities import Genero

load_dotenv()

def fetch_tmdb_genres(token: str, language: str = "es-ES"):
    base_url = "https://api.themoviedb.org/3"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }
    
    genres_dict = {}
    
    with httpx.Client(base_url=base_url, headers=headers) as client:
        # Fetch movie genres
        res_movie = client.get("/genre/movie/list", params={"language": language})
        res_movie.raise_for_status()
        for g in res_movie.json().get("genres", []):
            genres_dict[str(g["id"])] = g["name"]
            
        # Fetch tv genres
        res_tv = client.get("/genre/tv/list", params={"language": language})
        res_tv.raise_for_status()
        for g in res_tv.json().get("genres", []):
            genres_dict[str(g["id"])] = g["name"]
            
    return genres_dict

def populate():
    token = os.getenv("TMDB_READ_TOKEN")
    if not token:
        print("Error: TMDB_READ_TOKEN no configurado en .env")
        sys.exit(1)
        
    print("Obteniendo géneros de TMDB...")
    genres = fetch_tmdb_genres(token)
    
    print(f"Obtenidos {len(genres)} géneros únicos.")
    
    db = Database()
    db.init_db()
    
    print("Guardando en la base de datos...")
    with db.get_session() as session:
        for gid, name in genres.items():
            g = Genero(id=f"tmdb_{gid}", nombre=name)
            # Usar merge para insertar o actualizar sin errores de duplicados
            session.merge(g)
        session.commit()
        
    print("¡Géneros guardados exitosamente!")

if __name__ == "__main__":
    populate()
