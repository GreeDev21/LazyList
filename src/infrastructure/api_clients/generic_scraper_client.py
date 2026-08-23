import httpx
import logging
from selectolax.parser import HTMLParser
from typing import List, Dict, Any
from src.domain.ports.api_client import ApiClientPort

logger = logging.getLogger("lazylist")

class UrlScraperClient(ApiClientPort):
    """
    Cliente genérico para extraer metadatos estáticos de un recurso a partir de su URL.
    Utiliza httpx y selectolax para un parseo ultrarrápido sin ejecutar JS.
    """
    def __init__(self):
        # User-Agent común para evitar bloqueos básicos
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.client = httpx.Client(headers=self.headers, timeout=10.0, follow_redirects=True)

    def search(self, query: str, category: str) -> List[Dict[str, Any]]:
        # En el caso del Scraper Genérico, asumimos que "query" es directamente la URL que el usuario pegó.
        if category != "recursos":
            raise NotImplementedError("UrlScraperClient solo soporta 'recursos'")
            
        if not query.startswith("http"):
            return [] # No es una URL válida
            
        try:
            response = self.client.get(query)
            response.raise_for_status()
            
            tree = HTMLParser(response.text)
            
            # Priorizar OpenGraph tags
            og_title = tree.css_first('meta[property="og:title"]')
            title = og_title.attributes.get('content') if og_title else None
            
            if not title:
                title_node = tree.css_first('title')
                title = title_node.text() if title_node else query
                
            og_desc = tree.css_first('meta[property="og:description"]')
            desc = og_desc.attributes.get('content') if og_desc else ""
            
            if not desc:
                meta_desc = tree.css_first('meta[name="description"]')
                desc = meta_desc.attributes.get('content') if meta_desc else ""
                
            return [{
                "api_id": query, # Usamos la URL misma como ID
                "title": str(title).strip(),
                "year": "",
                "overview": str(desc).strip()
            }]
        except Exception as e:
            logger.error(f"Error scrapeando {query}: {e}", exc_info=True)
            return []

    def get_details(self, api_id: str, category: str) -> Dict[str, Any]:
        """api_id es la URL a scrapear"""
        if category != "recursos":
            raise NotImplementedError()
            
        # Para detalles, hacemos el mismo scrapeo (lo ideal sería guardarlo en cache desde la búsqueda, 
        # pero mantenemos la statelessness por ahora).
        results = self.search(api_id, category)
        if not results:
            return {
                "id": "url_" + str(hash(api_id)),
                "titulo": "Recurso Desconocido",
                "url": api_id,
                "descripcion": "",
                "tipo": "Link"
            }
            
        res = results[0]
        return {
            "id": "url_" + str(hash(api_id)),
            "titulo": res["title"],
            "url": api_id,
            "descripcion": res["overview"],
            "tipo": "Link"
        }
