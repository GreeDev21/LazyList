import os
import httpx
from dotenv import load_dotenv
import asyncio
import json

# Cargar las variables del .env
load_dotenv()

async def fetch_tmdb_sample():
    """Busca la película 'Inception' en TMDB para ver la estructura de datos."""
    print("\n=== TMDB (Películas) ===")
    token = os.getenv("TMDB_READ_TOKEN")
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    url = "https://api.themoviedb.org/3/search/movie?query=Inception&language=es-ES&page=1"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()
        # Mostramos solo el primer resultado para no ensuciar tanto la consola
        if data.get("results"):
            print(json.dumps(data["results"][0], indent=2, ensure_ascii=False))
        else:
            print("No se encontraron resultados.")

async def fetch_google_books_sample():
    """Busca 'El Señor de los Anillos' en Google Books."""
    print("\n=== Google Books (Libros) ===")
    url = "https://www.googleapis.com/books/v1/volumes?q=intitle:El+Señor+de+los+Anillos&maxResults=1"
    # Google Books no requiere API KEY estricta para búsquedas públicas simples.
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if data.get("items"):
            print(json.dumps(data["items"][0], indent=2, ensure_ascii=False))

async def fetch_anilist_sample():
    """Busca el anime 'Attack on Titan' usando GraphQL en AniList."""
    print("\n=== AniList (Anime/Manga) ===")
    # AniList usa GraphQL, no necesita API KEY para queries públicas
    query = '''
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        id
        title {
          romaji
          english
          native
        }
        status
        episodes
        genres
        averageScore
        coverImage {
          large
        }
      }
    }
    '''
    variables = {"search": "Attack on Titan"}
    url = "https://graphql.anilist.co"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"query": query, "variables": variables})
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))

async def main():
    print("Probando APIs para explorar las estructuras de datos JSON...")
    await fetch_tmdb_sample()
    await fetch_google_books_sample()
    await fetch_anilist_sample()
    print("\n¡Pruebas finalizadas! Podés usar las salidas JSON para armar tus tablas.")

if __name__ == "__main__":
    asyncio.run(main())
