import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class AniListClient(ApiClientPort):
    def __init__(self):
        self.url = "https://graphql.anilist.co"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.client = httpx.Client(headers=headers, timeout=10.0)

    def _format_date(self, date_dict: dict) -> str:
        """Convierte {year: 1997, month: 10, day: 7} a YYYY-MM-DD"""
        if not date_dict or not date_dict.get('year'):
            return ""
        y = date_dict.get('year')
        m = date_dict.get('month') or 1
        d = date_dict.get('day') or 1
        return f"{y}-{m:02d}-{d:02d}"

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        media_type = "ANIME" if category == "anime" else "MANGA"
        graphql_query = '''
        query ($search: String, $type: MediaType) {
            Page(page: 1, perPage: 10) {
                media(search: $search, type: $type) {
                    id
                    title {
                        romaji
                        userPreferred
                    }
                    startDate { year }
                    description
                }
            }
        }
        '''
        variables = {"search": query, "type": media_type}
        response = self.client.post(self.url, json={"query": graphql_query, "variables": variables})
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data["data"]["Page"]["media"]:
            year = str(item.get("startDate", {}).get("year", "")) if item.get("startDate") else ""
            title = item.get("title", {})
            title_display = title.get("userPreferred") or title.get("romaji") or ""
            
            results.append({
                "api_id": str(item["id"]),
                "title": title_display,
                "year": year,
                "overview": item.get("description", "")
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        media_type = "ANIME" if category == "anime" else "MANGA"
        graphql_query = '''
        query ($id: Int, $type: MediaType) {
            Media(id: $id, type: $type) {
                id
                title { romaji english }
                episodes
                chapters
                status
                genres
                startDate { year month day }
                endDate { year month day }
                coverImage { large }
            }
        }
        '''
        variables = {"id": int(api_id), "type": media_type}
        response = self.client.post(self.url, json={"query": graphql_query, "variables": variables})
        response.raise_for_status()
        
        item = response.json()["data"]["Media"]
        title_romaji = item.get("title", {}).get("romaji") or ""
        title_english = item.get("title", {}).get("english") or ""
        
        imagen_url = item.get("coverImage", {}).get("large") if item.get("coverImage") else None
        
        if category == "anime":
            return {
                "id": f"anilist_{api_id}",
                "title_romaji": title_romaji,
                "title_english": title_english,
                "episodios": item.get("episodes"),
                "status": item.get("status"),
                "genre": item.get("genres", []),
                "premiered": self._format_date(item.get("startDate")),
                "ended": self._format_date(item.get("endDate")),
                "imagen_url": imagen_url
            }
        elif category == "mangas":
            # Nota: Para el autor, el usuario indicó que combinaremos con MangaDex.
            # Por ahora devolvemos la estructura básica con autor None.
            return {
                "id": f"anilist_manga_{api_id}",
                "title_romaji": title_romaji,
                "title_english": title_english,
                "status": item.get("status"),
                "year": item.get("startDate", {}).get("year") if item.get("startDate") else None,
                "autor": None, 
                "capitulos": item.get("chapters"),
                "genre": item.get("genres", []),
                "imagen_url": imagen_url
            }
        else:
            raise NotImplementedError(f"Categoría {category} no soportada por AniList")
