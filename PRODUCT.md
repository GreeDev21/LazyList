# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Vanilla HTML5 + TailwindCSS + Heroicons served as static files by the FastAPI backend (per `implementation_plan.md`, confirmed by the user). No build step.

## Users

A single user — the owner — running the app locally on their own machine. The product is personal and private: one catalog, local SQLite storage, no accounts.

## Product Purpose

A personal media backlog tracker: keep a catalog of everything the owner wants to consume and has consumed across movies, series, anime, manga, comics, novels, books, resources (links), and games — enriched with real metadata (covers, directors, genres, status, duration) so the catalog reads like a curated collection, not a list of titles. Success means the catalog stays current with minimal effort and the collection is browsable at a glance.

## Positioning

The "lazy" catalog: entering an item takes one action. Paste a URL or text, or search a picker, and the app auto-resolves full metadata from external APIs and scraping before saving. A neighboring checklist app could not truthfully copy this — it stores user-typed titles; LazyList stores enriched, API-resolved records.

## Operating Context

- Runs locally: FastAPI serves the REST API and the static frontend; SQLite file (`lazylinks.db`) holds all data.
- Two-step data flow: interactive search (user picks from lightweight results) then fetch-by-ID detail call (e.g. TMDB `append_to_response=credits`) before saving.
- External API keys live in `.env` (e.g. TMDB read token); some integrations (AniList, Google Books) need no key.
- Manual entry is the fallback for anything the APIs can't resolve and for fully manual categories (comics, novels, recursos, juegos).
- External APIs: TMDB, TVMaze, AniList, MangaDex, ComicVine, Google Books, IGDB, YouTube; scraping via `httpx` + `selectolax` (static) and Playwright (dynamic), with OpenGraph + JSON-LD priority.

## Capabilities and Constraints

- Ten categories: peliculas, series (incl. `series_tvmaze`), anime, mangas, comics, novelas, libros, recursos, juegos.
- Backend currently implements `GET /api/search` and `POST /api/save`; list, delete, and settings endpoints are planned in `implementation_plan.md` but not yet built.
- Settings planned: hide/show NSFW content, grid vs. list view, cache cleanup.
- Genre homologue table (`generos`) maps API genre IDs to unified names.
- Clean Architecture (hexagonal): domain, application, infrastructure, api layers; TDD with pytest; parametrized SQL queries; secure CORS in production.
- UI copy is Spanish (project-wide language; plan's copy uses Rioplatense forms). Persona scope keeps code identifiers in English; UI strings are Spanish.
- Product name: **LazyList**. Legacy "LazyLinks" appears in `implementation_plan.md` and the FastAPI app title; future work should rename those to LazyList.
- Explicitly undecided: how list/delete/settings surfaces behave in detail; which item fields show in each view.

## Brand Commitments

- Name: LazyList (user decision, 2026-08-01).
- UI language: Spanish.
- The design direction committed in `implementation_plan.md` (Claymorphism on dark background `#0b0a16`, purple/rose/pastel accents, Inter typeface) is a documented commitment of the incumbent plan, recorded here as evidence for the future visual world.

## Evidence on Hand

- `schema.sql` — full relational schema (10 tables + genre junction tables).
- `implementation_plan.md` — architecture, API route plan, design system commitments.
- `api_explorer.py` and `scratch/fetch_all_samples.py`, `scratch/fetch_full_raw_samples.py` — API response samples.
- `src/` — working FastAPI backend with domain entities, application use cases, repositories, and API clients (TMDB, AniList, MangaDex, ComicVine, Google Books, TVMaze).
- `tests/` — unit and integration tests (pytest).
- `.env` — API keys present locally (TMDB at minimum); never committed.
- No real user data, testimonials, or public deployment exists; future work must not fabricate any.

## Product Principles

1. **Zero-friction input wins**: entering an item must be faster than updating a spreadsheet; paste and search-picker flows exist so the lazy promise holds.
2. **Enriched over manual**: whenever an API or scraper can supply metadata, prefer it; manual entry is the fallback, not the default.
3. **Personal, local, private**: single user, local SQLite, no accounts, no cloud dependency.
4. **Complete records**: the search-then-fetch-detail flow exists so every saved item is full, not a stub.
5. **Honest filtering**: NSFW content is storable but hidden by default behind an explicit setting.

## Accessibility & Inclusion

No product-specific accessibility requirement established beyond a general, cleanly contrastable interface (dark theme commitment in the plan). Spanish UI copy.
