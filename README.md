# LazyList · Tu Colección Personal

**LazyList** es una aplicación web minimalista y táctil diseñada para catalogar y gestionar tu biblioteca personal de juegos, películas, series, anime, mangas, cómics, novelas, libros y recursos web en un solo lugar. 

En lugar de abrumarte con recomendaciones automáticas y carruseles infinitos, LazyList propone un "estante virtual" claymórfico de portadas que vos controlás, resolviendo los metadatos de forma automática pegando una URL o buscando por título.

---

## 🏗️ Arquitectura y Tecnologías

El proyecto sigue los principios de **Clean Architecture (Arquitectura Hexagonal)** desacoplada en capas para facilitar el testeo y mantenimiento:

- **Frontend**: Vanilla HTML5, CSS con diseño Claymorphic Puro y JavaScript estructurado en [`static/`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static).
- **Backend**: FastAPI (Python 3.14) encargado de exponer las rutas REST y servir el frontend estático.
- **Base de Datos**: SQLite gestionado a través de SQLModel (ORM basado en Pydantic y SQLAlchemy).
- **Integraciones**: Clientes desacoplados para APIs externas como TMDB, AniList, Google Books, IGDB, ComicVine, y la API oficial de YouTube.

---

## 🛠️ Requisitos e Instalación

### 1. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables con tus claves correspondientes (ver el archivo de ejemplo o plantilla):
```ini
YOUTUBE_API_KEY=tu_google_api_key
TMDB_READ_TOKEN=tu_token_de_lectura_tmdb
GOOGLE_BOOKS_API_KEY=tu_google_api_key
# ... otras claves requeridas en src/infrastructure/api_clients/
```

### 2. Entorno Virtual de Python
Inicializa e instala las dependencias necesarias:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt  # O instala fastapi, sqlmodel, httpx, selectolax, pytest
```

### 3. Iniciar el Servidor de Desarrollo
Para arrancar el backend en modo reload automático:
```powershell
.venv\Scripts\uvicorn src.api.main:app --reload
```
Una vez iniciado, abre tu navegador en: **`http://127.0.0.1:8000`**

---

## 🧪 Pruebas (Suite de Tests)

El proyecto cuenta con pruebas unitarias y de integración locales que cubren las entidades, casos de uso y clientes de red:

Para correr todas las pruebas locales:
```powershell
.venv\Scripts\python -m pytest -v
```

---

## 📂 Documentación Adicional

- [**`TODO.md`**](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/TODO.md): Listado estructurado de tareas pendientes y control de errores del desarrollo.
- [**`docs/como_leer_los_logs.md`**](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/docs/como_leer_los_logs.md): Guía práctica para comprender la trazabilidad y la lectura de tracebacks en la consola.
- [**`DESIGN.md`**](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/DESIGN.md): Lineamientos estéticos del diseño Claymorphism e interacciones.
- [**`PRODUCT.md`**](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/PRODUCT.md): Especificación del producto y flujos del usuario.
