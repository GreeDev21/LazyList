import os
import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class ComicVineClient(ApiClientPort):
    def __init__(self):
        self.base_url = "https://comicvine.gamespot.com/api"
        self.api_key = os.getenv("COMICVINE_API_KEY")
        if not self.api_key:
            raise ValueError("COMICVINE_API_KEY no configurada en el .env")
            
        # ComicVine exige un User-Agent identificatorio
        headers = {"User-Agent": "LazyListApp/1.0 (Personal Content Tracker)"}
        self.client = httpx.Client(base_url=self.base_url, headers=headers, timeout=15.0)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "comics":
            raise NotImplementedError(f"ComicVine solo soporta 'comics'")
            
        response = self.client.get("/search/", params={
            "api_key": self.api_key,
            "format": "json",
            "resources": "volume", # Los comics serializados se guardan como "volumes" en ComicVine
            "query": query,
            "limit": 10
        })
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "api_id": str(item["id"]),
                "title": item.get("name") or "",
                "year": str(item.get("start_year", "")),
                "overview": str(item.get("count_of_issues", "0")) + " issues" 
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "comics":
            raise NotImplementedError()
            
        response = self.client.get(f"/volume/4050-{api_id}/", params={
            "api_key": self.api_key,
            "format": "json"
        })
        response.raise_for_status()
        
        item = response.json().get("results", {})
        
        people = item.get("people", [])
        escritor_str = None
        if people:
            names = [p.get("name") for p in people[:3] if p.get("name")]
            escritor_str = ", ".join(names)
            if len(people) > 3:
                escritor_str += " y otros"
                
        return {
            "id": f"cvine_{api_id}",
            "title": item.get("name", ""),
            "year": int(item.get("start_year")) if item.get("start_year") else None,
            "publisher": item.get("publisher", {}).get("name") if item.get("publisher") else None,
            "capitulos": item.get("count_of_issues"),
            "escritor": escritor_str,
            "status": "Ended" if item.get("count_of_issues", 0) > 0 else "Ongoing" # Heurística básica
        }
