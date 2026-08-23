import os
import httpx
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

ARTIFACT_PATH = r"C:\Users\aguse\.gemini\antigravity\brain\37feacf3-fc71-418f-9eae-56585c560104\api_structures.md"

async def fetch_json(client, url, headers=None, params=None):
    try:
        resp = await client.get(url, headers=headers, params=params, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

async def main():
    async with httpx.AsyncClient() as client:
        with open(ARTIFACT_PATH, "w", encoding="utf-8") as f:
            f.write("# Estructuras de Datos de las APIs\n\n")
            f.write("Acá tenés una muestra de la estructura de datos real que devuelve cada API para el primer elemento de tus listas, para que puedas diseñar la Base de Datos.\n\n")

            # --- PELICULAS: The Batman (TMDB) ---
            f.write("## 🎬 Películas (Ej: The Batman) - TMDB\n")
            tmdb_token = os.getenv("TMDB_READ_TOKEN")
            headers = {"Authorization": f"Bearer {tmdb_token}", "accept": "application/json"}
            data = await fetch_json(client, "https://api.themoviedb.org/3/search/movie", headers=headers, params={"query": "The batman", "language": "es-ES"})
            if data.get("results"):
                f.write("```json\n" + json.dumps(data["results"][0], indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- SERIES: Breaking Bad (TMDB -> TvMaze) ---
            f.write("## 📺 Series (Ej: Breaking Bad)\n")
            f.write("### 1. TMDB\n")
            data = await fetch_json(client, "https://api.themoviedb.org/3/search/tv", headers=headers, params={"query": "Breaking Bad", "language": "es-ES"})
            if data.get("results"):
                f.write("```json\n" + json.dumps(data["results"][0], indent=2, ensure_ascii=False) + "\n```\n\n")
            
            f.write("### 2. TvMaze\n")
            data = await fetch_json(client, "https://api.tvmaze.com/search/shows", params={"q": "Breaking Bad"})
            if data and isinstance(data, list):
                f.write("```json\n" + json.dumps(data[0], indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- ANIME: El heroe del escudo (AniList) ---
            f.write("## 🌸 Anime (Ej: El heroe del escudo) - AniList\n")
            query = '''query ($search: String) { Media (search: $search, type: ANIME) { id title { romaji english native } status episodes genres averageScore coverImage { large } } }'''
            resp = await client.post("https://graphql.anilist.co", json={"query": query, "variables": {"search": "Tate no Yuusha no Nariagari"}})
            f.write("```json\n" + json.dumps(resp.json(), indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- LIBROS: Soft Skills (Google Books) ---
            f.write("## 📚 Libros (Ej: Soft Skills John Sonmez) - Google Books\n")
            data = await fetch_json(client, "https://www.googleapis.com/books/v1/volumes", params={"q": "Soft Skills John Sonmez"})
            if data.get("items"):
                f.write("```json\n" + json.dumps(data["items"][0], indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- MANGA: Berserk (MangaDex -> AniList -> MangaUpdates) ---
            f.write("## 🗡️ Manga (Ej: Berserk)\n")
            f.write("### 1. MangaDex\n")
            data = await fetch_json(client, "https://api.mangadex.org/manga", params={"title": "Berserk", "limit": 1})
            if data.get("data"):
                f.write("```json\n" + json.dumps(data["data"][0], indent=2, ensure_ascii=False) + "\n```\n\n")

            f.write("### 2. AniList\n")
            query_manga = '''query ($search: String) { Media (search: $search, type: MANGA) { id title { romaji english } chapters volumes genres } }'''
            resp = await client.post("https://graphql.anilist.co", json={"query": query_manga, "variables": {"search": "Berserk"}})
            f.write("```json\n" + json.dumps(resp.json(), indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- COMIC: Absolute Batman (ComicVine) ---
            f.write("## 🦸‍♂️ Cómics (Ej: Absolute Batman) - ComicVine\n")
            cv_key = os.getenv("COMICVINE_API_KEY")
            # ComicVine needs a custom user-agent
            headers_cv = {"User-Agent": "LazyList/1.0"}
            data = await fetch_json(client, "https://comicvine.gamespot.com/api/search/", headers=headers_cv, params={"api_key": cv_key, "format": "json", "resources": "volume", "query": "Absolute Batman", "limit": 1})
            if data.get("results") and isinstance(data.get("results"), list) and len(data["results"]) > 0:
                f.write("```json\n" + json.dumps(data["results"][0], indent=2, ensure_ascii=False) + "\n```\n\n")
            else:
                f.write("```json\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n```\n\n")

if __name__ == "__main__":
    asyncio.run(main())
