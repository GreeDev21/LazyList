import os
import httpx
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

ARTIFACT_PATH = r"C:\Users\aguse\.gemini\antigravity\brain\37feacf3-fc71-418f-9eae-56585c560104\api_structures_full_raw.md"

async def fetch_json(client, url, headers=None, params=None):
    try:
        resp = await client.get(url, headers=headers, params=params, timeout=15)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

async def main():
    items = {
        "Peliculas": ["The batman", "La odisea"],
        "Series": ["Breaking Bad", "The witcher"],
        "Anime": ["Tate no Yuusha no Nariagari", "Sousou no frieren"], # Romaji para AniList
        "Libros": ["Soft Skills John Sonmez", "Principios de Economía Francisco Mochón"],
        "Novelas": ["Solo leveling", "Shadow Slave"],
        "Manga": ["Berserk", "Shiori Experience"],
        "Comic": ["Absolute Batman", "Absolute Flash"]
    }

    async with httpx.AsyncClient() as client:
        with open(ARTIFACT_PATH, "w", encoding="utf-8") as f:
            f.write("# Estructuras Crudas (RAW) de las APIs\n\n")
            f.write("Resultados completos y sin filtrar (2 ejemplos por categoría).\n\n")

            # --- PELICULAS ---
            f.write("## 🎬 Películas (TMDB)\n")
            tmdb_token = os.getenv("TMDB_READ_TOKEN")
            headers = {"Authorization": f"Bearer {tmdb_token}", "accept": "application/json"}
            for item in items["Peliculas"]:
                f.write(f"### {item}\n")
                data = await fetch_json(client, "https://api.themoviedb.org/3/search/movie", headers=headers, params={"query": item, "language": "es-ES"})
                f.write("```json\n" + json.dumps(data.get("results", [data])[0] if data.get("results") else data, indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- SERIES ---
            f.write("## 📺 Series\n")
            for item in items["Series"]:
                f.write(f"### {item}\n")
                f.write("#### TMDB\n")
                data = await fetch_json(client, "https://api.themoviedb.org/3/search/tv", headers=headers, params={"query": item, "language": "es-ES"})
                f.write("```json\n" + json.dumps(data.get("results", [data])[0] if data.get("results") else data, indent=2, ensure_ascii=False) + "\n```\n\n")
                f.write("#### TvMaze\n")
                data = await fetch_json(client, "https://api.tvmaze.com/search/shows", params={"q": item})
                f.write("```json\n" + json.dumps(data[0] if data and isinstance(data, list) else data, indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- ANIME ---
            f.write("## 🌸 Anime (AniList)\n")
            query_anime = '''query ($search: String) { Media (search: $search, type: ANIME) { id idMal title { romaji english native userPreferred } type format status description startDate { year month day } endDate { year month day } season seasonYear episodes duration chapters volumes countryOfOrigin isLicensed source hashtag trailer { id site thumbnail } updatedAt coverImage { extraLarge large medium color } bannerImage genres synonyms averageScore meanScore popularity isLocked trending favorites isAdult } }'''
            for item in items["Anime"]:
                f.write(f"### {item}\n")
                resp = await client.post("https://graphql.anilist.co", json={"query": query_anime, "variables": {"search": item}})
                f.write("```json\n" + json.dumps(resp.json(), indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- LIBROS ---
            f.write("## 📚 Libros (Google Books)\n")
            for item in items["Libros"]:
                f.write(f"### {item}\n")
                data = await fetch_json(client, "https://www.googleapis.com/books/v1/volumes", params={"q": item})
                f.write("```json\n" + json.dumps(data.get("items", [data])[0] if data.get("items") else data, indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- NOVELAS Y MANGA ---
            for cat in ["Novelas", "Manga"]:
                f.write(f"## 🗡️ {cat}\n")
                for item in items[cat]:
                    f.write(f"### {item}\n")
                    f.write("#### MangaDex\n")
                    data = await fetch_json(client, "https://api.mangadex.org/manga", params={"title": item, "limit": 1})
                    f.write("```json\n" + json.dumps(data.get("data", [data])[0] if data.get("data") else data, indent=2, ensure_ascii=False) + "\n```\n\n")
                    
                    f.write("#### AniList\n")
                    query_manga = '''query ($search: String) { Media (search: $search, type: MANGA) { id idMal title { romaji english native } type format status description chapters volumes coverImage { large color } genres averageScore isAdult } }'''
                    resp = await client.post("https://graphql.anilist.co", json={"query": query_manga, "variables": {"search": item}})
                    f.write("```json\n" + json.dumps(resp.json(), indent=2, ensure_ascii=False) + "\n```\n\n")

            # --- COMIC ---
            f.write("## 🦸‍♂️ Cómics (ComicVine)\n")
            cv_key = os.getenv("COMICVINE_API_KEY")
            headers_cv = {"User-Agent": "LazyList/1.0"}
            for item in items["Comic"]:
                f.write(f"### {item}\n")
                data = await fetch_json(client, "https://comicvine.gamespot.com/api/search/", headers=headers_cv, params={"api_key": cv_key, "format": "json", "resources": "volume", "query": item, "limit": 1})
                f.write("```json\n" + json.dumps(data.get("results", [data])[0] if data.get("results") else data, indent=2, ensure_ascii=False) + "\n```\n\n")

if __name__ == "__main__":
    asyncio.run(main())
