import os
import re
import httpx
from typing import List, Dict, Any
from urllib.parse import urlparse, parse_qs
from src.domain.ports.api_client import ApiClientPort

class YouTubeApiClient(ApiClientPort):
    """
    Cliente para la API de YouTube Data v3.
    Se encarga de procesar URLs de videos y extraer metadatos estructurados.
    """
    def __init__(self):
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def extract_video_id(self, url: str) -> str:
        """
        Extrae el ID del video de YouTube a partir de la URL provista.
        """
        if not url:
            return ""
        
        # Patrones comunes de URL de YouTube
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\s]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([^?\s]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?\s]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([^?\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
                
        # Fallback usando urllib
        try:
            parsed = urlparse(url)
            if 'youtube.com' in parsed.netloc:
                qs = parse_qs(parsed.query)
                if 'v' in qs:
                    return qs['v'][0]
        except Exception:
            pass
            
        return ""

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        if category != "recursos":
            raise NotImplementedError("YouTubeApiClient solo soporta recursos")
            
        video_id = self.extract_video_id(query)
        if not video_id:
            return []
            
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY no configurado en variables de entorno")
            
        params = {
            "part": "snippet",
            "id": video_id,
            "key": self.api_key
        }
        
        response = self.client.get("/videos", params=params)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        if not items:
            return []
            
        snippet = items[0].get("snippet", {})
        return [{
            "api_id": query, # La URL completa actúa como ID único para el recurso
            "title": snippet.get("title", ""),
            "year": "",
            "overview": snippet.get("description", "")
        }]

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        if category != "recursos":
            raise NotImplementedError("YouTubeApiClient solo soporta recursos")
            
        video_id = self.extract_video_id(api_id)
        if not video_id:
            raise ValueError(f"No se pudo extraer el ID de video de la URL: {api_id}")
            
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY no configurado en variables de entorno")
            
        params = {
            "part": "snippet",
            "id": video_id,
            "key": self.api_key
        }
        
        response = self.client.get("/videos", params=params)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        if not items:
            raise ValueError(f"No se encontró información para el video: {video_id}")
            
        snippet = items[0].get("snippet", {})
        
        thumbnails = snippet.get("thumbnails") or {}
        imagen_url = (
            thumbnails.get("high", {}).get("url") or 
            thumbnails.get("medium", {}).get("url") or 
            thumbnails.get("default", {}).get("url")
        )
        
        return {
            "id": f"yt_{video_id}",
            "titulo": snippet.get("title", ""),
            "url": api_id,
            "creado_autor": snippet.get("channelTitle", ""),
            "volver_a_ver": False,
            "notas": "",
            "imagen_url": imagen_url
        }
