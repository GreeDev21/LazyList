import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class TvMazeClient(ApiClientPort):
    def __init__(self):
        self.base_url = "https://api.tvmaze.com"
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "series_tvmaze":
            raise NotImplementedError("TvMaze solo soporta series")
            
        response = self.client.get("/search/shows", params={"q": query})
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data:
            show = item.get("show", {})
            year = show.get("premiered", "").split("-")[0] if show.get("premiered") else ""
            
            results.append({
                "api_id": str(show.get("id")),
                "title": show.get("name", ""),
                "year": year,
                "overview": show.get("summary", "")
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "series_tvmaze":
            raise NotImplementedError()
            
        response = self.client.get(f"/shows/{api_id}")
        response.raise_for_status()
        
        show = response.json()
        
        imagen = show.get("image") or {}
        imagen_url = imagen.get("medium")
        
        return {
            "id": f"tvm_{api_id}",
            "title": show.get("name"),
            "original_title": show.get("name"), # TvMaze doesn't separate original heavily
            "status": show.get("status"),
            "premiered": show.get("premiered"),
            "ended": show.get("ended"),
            "plataform": show.get("network", {}).get("name") if show.get("network") else (show.get("webChannel", {}).get("name") if show.get("webChannel") else None),
            "origin_country": [show.get("network", {}).get("country", {}).get("code")] if show.get("network") and show.get("network").get("country") else [],
            "genre": show.get("genres", []),
            "imagen_url": imagen_url
        }
