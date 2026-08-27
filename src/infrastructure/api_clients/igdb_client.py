import os
import httpx
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

class IGDBClient(ApiClientPort):
    def __init__(self):
        self.client_id = os.getenv("TWITCH_CLIENT_ID")
        self.client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.access_token = None
        self.base_url = "https://api.igdb.com/v4"
        self.client = httpx.Client(timeout=15.0)

    def _authenticate(self):
        """Autenticación OAuth 2.0 con Twitch para obtener el token de IGDB."""
        if not self.client_id or not self.client_secret:
            raise ValueError("Las credenciales TWITCH_CLIENT_ID y TWITCH_CLIENT_SECRET no están configuradas.")
            
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials"
        response = self.client.post(url)
        response.raise_for_status()
        self.access_token = response.json().get("access_token")

    def _get_headers(self):
        if not self.access_token:
            self._authenticate()
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "juegos":
            raise NotImplementedError("IGDBClient solo soporta 'juegos'")
            
        # IGDB usa un body en texto plano tipo "SQL" para sus consultas
        body = f'search "{query}"; fields name, first_release_date, summary; limit 10;'
        response = self.client.post(
            f"{self.base_url}/games",
            headers=self._get_headers(),
            content=body
        )
        response.raise_for_status()
        
        results = []
        for item in response.json():
            from datetime import datetime
            year = ""
            if item.get("first_release_date"):
                year = str(datetime.fromtimestamp(item["first_release_date"]).year)
                
            results.append({
                "api_id": str(item["id"]),
                "title": item.get("name", ""),
                "year": year,
                "overview": item.get("summary", "")
            })
        return results

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "juegos":
            raise NotImplementedError()
            
        body = f'where id = {api_id}; fields name, genres.name, platforms.name, first_release_date, involved_companies.company.name, involved_companies.publisher, websites.*, cover.url;'
        response = self.client.post(
            f"{self.base_url}/games",
            headers=self._get_headers(),
            content=body
        )
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise ValueError("Juego no encontrado")
            
        item = data[0]
        
        from datetime import datetime
        year = None
        if item.get("first_release_date"):
            year = datetime.fromtimestamp(item["first_release_date"]).year
            
        publisher = None
        for company in item.get("involved_companies", []):
            if company.get("publisher") and company.get("company"):
                publisher = company["company"].get("name")
                break
                
        generos = [g["name"] for g in item.get("genres", [])]
        plataformas = [p["name"] for p in item.get("platforms", [])]
        
        tiendas_encontradas = []
        tiendas_map = {
            13: "Steam",
            16: "Epic Games",
            17: "GOG"
        }
        for website in item.get("websites", []):
            # IGDB docs refer to 'category', but the API sometimes returns 'type'
            cat = website.get("category") or website.get("type")
            if cat in tiendas_map:
                nombre_tienda = tiendas_map[cat]
                if nombre_tienda not in tiendas_encontradas:
                    tiendas_encontradas.append(nombre_tienda)
        
        tienda = ", ".join(tiendas_encontradas) if tiendas_encontradas else None
        
        cover_url = item.get("cover", {}).get("url")
        imagen_url = None
        if cover_url:
            # IGDB retorna URLs relativas al protocolo como '//images.igdb.com/...'
            if cover_url.startswith("//"):
                cover_url = "https:" + cover_url
            imagen_url = cover_url.replace("t_thumb", "t_cover_big")
            
        return {
            "id": f"igdb_{api_id}",
            "titulo": item.get("name", ""),
            "tienda": tienda,
            "imagen_url": imagen_url
        }
