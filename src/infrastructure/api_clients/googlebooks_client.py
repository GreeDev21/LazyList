import os
import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class GoogleBooksClient(ApiClientPort):
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1"
        self.api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "libros":
            raise NotImplementedError("GoogleBooks solo soporta libros")
            
        params = {"q": query}
        if self.api_key:
            params["key"] = self.api_key
            
        response = self.client.get("/volumes", params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data.get("items", []):
            vol = item.get("volumeInfo", {})
            results.append({
                "api_id": item.get("id"),
                "title": vol.get("title", ""),
                "year": vol.get("publishedDate", "").split("-")[0] if vol.get("publishedDate") else "",
                "overview": vol.get("description", "")
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "libros":
            raise NotImplementedError()
            
        params = {}
        if self.api_key:
            params["key"] = self.api_key
            
        response = self.client.get(f"/volumes/{api_id}", params=params)
        response.raise_for_status()
        
        vol = response.json().get("volumeInfo", {})
        
        year_str = vol.get("publishedDate", "").split("-")[0]
        year = int(year_str) if year_str.isdigit() else None
        
        imagen_url = vol.get("imageLinks", {}).get("thumbnail") if vol.get("imageLinks") else None
        
        return {
            "id": f"gb_{api_id}",
            "titulo": vol.get("title", ""),
            "autor": vol.get("authors", [""])[0] if vol.get("authors") else None,
            "ano": year,
            "genero": vol.get("categories", []),
            "saga": None, # Google books rara vez da la saga estructurada
            "orden": None,
            "imagen_url": imagen_url
        }
