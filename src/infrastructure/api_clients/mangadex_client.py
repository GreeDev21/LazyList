import os
import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class MangaDexClient(ApiClientPort):
    def __init__(self):
        self.base_url = "https://api.mangadex.org"
        self.token = os.getenv("MANGADEX_SECRET")
        
        headers = {"User-Agent": "LazyList/1.0"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            
        self.client = httpx.Client(base_url=self.base_url, headers=headers, timeout=10.0)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "mangas":
            raise NotImplementedError(f"MangaDex solo soporta la categoría 'mangas', no '{category}'")
            
        # order[relevance]=desc para mejores resultados
        response = self.client.get("/manga", params={"title": query, "limit": 10, "order[relevance]": "desc"})
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data.get("data", []):
            attrs = item.get("attributes", {})
            title_dict = attrs.get("title", {})
            title = title_dict.get("en") or title_dict.get("ja-ro") or list(title_dict.values())[0] if title_dict else ""
            
            # Extract description
            desc_dict = attrs.get("description", {})
            overview = desc_dict.get("en") or desc_dict.get("es") or ""
            if not overview and desc_dict:
                overview = list(desc_dict.values())[0]

            results.append({
                "api_id": str(item["id"]),
                "title": title,
                "year": str(attrs.get("year", "")),
                "overview": overview[:200] + "..." if len(overview) > 200 else overview
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "mangas":
            raise NotImplementedError(f"MangaDex solo soporta la categoría 'mangas'")
            
        # Usamos includes[]=author para que MangaDex nos mande los datos del autor incrustados
        response = self.client.get(f"/manga/{api_id}", params={"includes[]": "author"})
        response.raise_for_status()
        
        item = response.json()["data"]
        attrs = item.get("attributes", {})
        
        title_dict = attrs.get("title", {})
        title_romaji = title_dict.get("ja-ro") or title_dict.get("en") or list(title_dict.values())[0] if title_dict else ""
        
        # El título en inglés a veces viene en altTitles
        title_english = None
        for alt in attrs.get("altTitles", []):
            if "en" in alt:
                title_english = alt["en"]
                break
                
        # Extraer autor desde las relaciones (relationships)
        autor_name = None
        for rel in item.get("relationships", []):
            if rel.get("type") == "author" and "attributes" in rel:
                autor_name = rel["attributes"].get("name")
                break
                
        return {
            "id": f"mdex_{api_id}",
            "title_romaji": title_romaji,
            "title_english": title_english,
            "status": attrs.get("status"),
            "year": attrs.get("year"),
            "autor": autor_name,
            "capitulos": None, # MangaDex no da el conteo total fácilmente, se requiere endpoint /aggregate
            "genre": [t["attributes"]["name"].get("en") for t in attrs.get("tags", []) if t.get("attributes", {}).get("group") == "genre"]
        }
