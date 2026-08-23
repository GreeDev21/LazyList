import os
import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class TMDBClient(ApiClientPort):
    def __init__(self):
        self.token = os.getenv("TMDB_READ_TOKEN")
        if not self.token:
            raise ValueError("TMDB_READ_TOKEN no está configurado en las variables de entorno.")
            
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json"
        }
        self.base_url = "https://api.themoviedb.org/3"
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, timeout=10.0)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category == "peliculas":
            endpoint = "/search/movie"
        elif category == "series":
            endpoint = "/search/tv"
        else:
            raise NotImplementedError(f"TMDB no soporta la categoría: {category}")
            
        response = self.client.get(endpoint, params={"query": query, "language": "es-ES"})
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("results", []):
            year = ""
            if category == "peliculas" and item.get("release_date"):
                year = item["release_date"].split("-")[0]
            elif category == "series" and item.get("first_air_date"):
                year = item["first_air_date"].split("-")[0]
                
            results.append({
                "api_id": str(item["id"]),
                "title": item.get("title") or item.get("name"),
                "year": year,
                "overview": item.get("overview", "")
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category == "peliculas":
            response = self.client.get(f"/movie/{api_id}", params={"language": "es-ES", "append_to_response": "credits"})
            response.raise_for_status()
            data = response.json()
            
            # Extraer director
            director = None
            credits = data.get("credits", {}).get("crew", [])
            for person in credits:
                if person.get("job") == "Director":
                    director = person.get("name")
                    break
                    
            return {
                "id": f"tmdb_{api_id}",
                "title": data.get("title"),
                "original_title": data.get("original_title"),
                "release_date": data.get("release_date"),
                "director": director,
                "duracion": data.get("runtime"),
                "origin_country": data.get("origin_country", []),
                "genre": [g["name"] for g in data.get("genres", [])]
            }
            
        elif category == "series":
            response = self.client.get(f"/tv/{api_id}", params={"language": "es-ES"})
            response.raise_for_status()
            data = response.json()
            
            return {
                "id": f"tmdb_tv_{api_id}",
                "title": data.get("name"),
                "original_title": data.get("original_name"),
                "status": data.get("status"),
                "premiered": data.get("first_air_date"),
                "ended": data.get("last_air_date"),
                "plataform": ", ".join([n["name"] for n in data.get("networks", [])]) if data.get("networks") else None,
                "origin_country": data.get("origin_country", []),
                "genre": [g["name"] for g in data.get("genres", [])]
            }
        else:
            raise NotImplementedError(f"Categoría {category} no soportada")
