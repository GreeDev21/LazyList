# LazyList - Control de Errores y Tareas Pendientes (TODO)

Este documento centraliza los problemas detectados en la libreta de anotaciones y las dudas de desarrollo. Se utiliza una plantilla estructurada para garantizar que cada tarea tenga un objetivo claro de resolución antes de empezar a picar código.

---

## Plantilla Recomendada (Tarjetas de Tarea Estructurada)

Para cada issue o tarea, completamos los siguientes tres campos:

```markdown
### [ ] TÍTULO_CORTO_DE_LA_TAREA
- **Problema:** Descripción clara del bug, feature o comportamiento inesperado.
- **Razón / Contexto:** Por qué ocurre o por qué es necesario hacer este cambio (si no es autoexplicativo).
- **Definición de Hecho (DoD):** Criterios específicos y medibles que deben cumplirse para dar la tarea por solucionada.
```

---

## Tareas Pendientes (Notebook)

A continuación se estructuran los ítems de tu libreta bajo el formato propuesto, incorporando los hallazgos tras revisar el código del proyecto:

### [x] Frontend no identificado en la arquitectura
- **Problema:** Dudas sobre la ubicación física del frontend.
- **Razón / Contexto:** Al abrir el proyecto no queda claro a primera vista dónde se ubica la UI respecto a la estructura de carpetas de Python (`src/domain`, `src/infrastructure`).
- **Definición de Hecho (DoD):**
  - [x] Ubicar los archivos frontend: confirmados en el directorio `/static` ([`index.html`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/index.html), [`style.css`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/style.css), [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js)). FastAPI los monta en [`main.py`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/api/main.py#L63).
  - [x] Documentar detalladamente esta arquitectura en [`docs/arquitectura.md`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/docs/arquitectura.md) para evitar futuras confusiones.

### [x] Comportamiento y origen de datos de YouTube
- **Problema:** Cargar un video de YouTube no extrae el nombre del canal.
- **Razón / Contexto:** Actualmente **no** se usa la API oficial de YouTube. El sistema usa un scraper estático genérico (`UrlScraperClient` en [`generic_scraper_client.py`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/infrastructure/api_clients/generic_scraper_client.py)) que procesa etiquetas OpenGraph (`og:title`, `og:description`) con la librería `selectolax` de forma síncrona. Como YouTube se renderiza vía JS y bloquea bots básicos, no se obtiene el canal sin consultar la API o utilizar un parser dedicado.
- **Definición de Hecho (DoD):**
  - [x] Decidir si se implementará la API de YouTube oficial o si se extenderá el scraper para interceptar metadata de canales en URLs de tipo `youtube.com/watch` / `youtu.be`.
  - [x] Lograr que, al ingresar un enlace de YouTube, el campo "Autor" u homólogo se complete automáticamente con el nombre del canal.



### [x] Modal de detalle con datos hardcodeados
- **Problema:** El modal de detalle del ítem muestra información genérica cableada en el HTML.
- **Razón / Contexto:** En [`index.html`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/index.html#L181-L257), el modal `<dialog id="detail-dialog">` incluye datos estáticos como "Absolute Batman" y "DC Comics". Si el JS no los reemplaza correctamente para ciertos tipos de categorías, el usuario ve placeholders confusos.
- **Definición de Hecho (DoD):**
  - [x] Asegurar que el cargador del modal en [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js) limpie o reemplace el 100% de los placeholders estáticos al abrir cualquier elemento.
  - [x] Comprobar que no queden textos hardcodeados de ejemplo visibles al abrir el modal de un ítem vacío o recién creado.

### [x] Botón para carga manual y opción masiva
- **Problema:** Se necesita poder agregar elementos uno por uno y también en lote (bulk).
- **Razón / Contexto:** Agilizar la carga inicial cuando se migran listas grandes de contenido desde otras plataformas.
- **Definición de Hecho (DoD):**
  - [x] Diseñar y programar una interfaz (dentro del modal manual o en una vista dedicada) para pegar múltiples líneas/URLs/títulos.
  - [x] Modificar el endpoint del backend para procesar colecciones de ítems y retornarlos de forma eficiente en un solo batch.

### [x] Eliminación de opciones NSFW
- **Problema:** Quitar las opciones y marcas NSFW de la aplicación.
- **Razón / Contexto:** Decisión de uso: no se guardará contenido adulto y se quiere evitar la visualización accidental de marcas relacionadas.
- **Definición de Hecho (DoD):**
  - [x] Remover el campo `NSFW` del modelo [`Recurso`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py) en el backend y limpiar las tablas.
  - [x] Eliminar badges, botones de filtro y estilos visuales NSFW en [`index.html`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/index.html) y [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js).

### [x] Centrar modal y adaptar detalles por categoría
- **Problema:** El modal no se posiciona en el centro de la pantalla y la estructura de los campos no varía según la categoría del ítem.
- **Razón / Contexto:** Estética y experiencia de usuario (UX): un juego necesita ficha de "tienda/mod" mientras que un libro requiere "saga/autor".
- **Definición de Hecho (DoD):**
  - [x] Centrar los `<dialog>` utilizando Flexbox/Grid o posicionamiento absoluto centrado en CSS [`style.css`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/style.css).
  - [x] Implementar lógica dinámica en [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js) para ocultar/mostrar secciones de la ficha editorial según la categoría activa del elemento.

### [x] Logs y trazabilidad del sistema
- **Problema:** Falta de logs del servidor ante fallos o llamadas API externas.
- **Razón / Contexto:** Es crítico diagnosticar fallos silenciosos cuando las APIs de terceros (como Anilist, ComicVine, etc.) cambian de contrato o fallan.
- **Definición de Hecho (DoD):**
  - [x] Configurar el módulo `logging` nativo de Python en FastAPI.
  - [x] Añadir logs en los bloques `try/except` críticos de los clientes de APIs externas ([`src/infrastructure/api_clients`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/infrastructure/api_clients)).

### [x] Detectar tipos de recursos (webs, playlist, artículos)
- **Problema:** Analizar si realmente vale la pena categorizar los recursos por tipo.
- **Razón / Contexto:** Nota escrita en libreta de la cual no se recuerda la motivación exacta.
- **Definición de Hecho (DoD):**
  - [x] Definir si aporta valor clasificar un "recurso" o si con la URL y la descripción general ya es suficiente. Si se descarta, eliminar la columna `tipo` de la entidad [`Recurso`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py#L106).

### [x] Revisar formulario de carga manual
- **Problema:** El formulario manual es muy genérico y no permite parametrizar datos finos.
- **Razón / Contexto:** Consecuencia del ítem de géneros vacíos en cómics: si la carga manual no expone campos específicos de la categoría seleccionada, la base de datos queda incompleta.
- **Definición de Hecho (DoD):**
  - [x] Modificar el formulario de carga manual para que al cambiar de categoría muestre u oculte inputs específicos (ej. escritor para cómics, autor para libros, url para recursos).

### [x] Obtener imágenes para los ítems guardados
- **Problema:** Los elementos guardados en la colección no muestran o no resuelven correctamente sus imágenes de portada/preview asociadas desde las APIs externas o el scraping.
- **Razón / Contexto:** Para lograr la experiencia claymórfica visual tipo "estante de colección", cada tarjeta necesita mostrar la portada real del libro, juego, película o recurso en lugar de un marcador genérico de color.
- **Definición de Hecho (DoD):**
  - [x] Verificar que los clientes de API externa extraigan y retornen las URLs de las imágenes de portada (ej. TMDB poster_path, Google Books imageLinks, IGDB cover, etc.).
  - [x] Guardar la URL o referencia de la imagen en la base de datos para cada entidad correspondiente en `src/domain/entities.py`.
  - [x] Adaptar el frontend (`app.js` y `index.html`) para renderizar las imágenes de portada en la grilla y el modal de detalle, incluyendo un fallback de gradiente de color cuando no haya imagen disponible.

---

## Tareas Críticas de Seguridad (¡IMPORTANTE!)

### [x] Fuga de Credenciales y Secretos (Alerta GitGuardian)
- **Problema:** GitGuardian detectó nombres de usuario, correos electrónicos o secretos (tokens y API keys) expuestos públicamente al cambiar la visibilidad del repositorio a público.
- **Razón / Contexto:** Subir secretos al historial de Git expone las credenciales a bots automatizados que escanean repositorios públicos de manera constante. Las claves afectadas deben ser revocadas inmediatamente.
- **Definición de Hecho (DoD):**
  - [x] **Rotar Claves (CRÍTICO):** Invalidar y re-generar inmediatamente todas las claves/tokens en los proveedores de las APIs afectadas (TMDB, YouTube, Twitch/IGDB, ComicVine, etc.). *Considerar las claves viejas comprometidas*.
  - [x] **Revisar `.gitignore`:** Asegurar que `.env`, `lazylinks.db` y otros archivos sensibles estén listados en el `.gitignore` y no estén siendo rastreados en Git.
  - [x] **Limpiar Historial de Git:** Ejecutar una purga del historial de commits usando herramientas como `git-filter-repo` o BFG Repo-Cleaner para remover físicamente los archivos sensibles del historial histórico.

---

## Nuevas Ideas y Características Pendientes

### [ ] Buscador interno de la colección
- **Problema:** No se puede buscar un elemento específico dentro de la colección guardada localmente.
- **Razón / Contexto:** A medida que la biblioteca crece, se vuelve difícil encontrar un ítem desplazándose manualmente por la grilla.
- **Definición de Hecho (DoD):**
  - [ ] Diseñar e incorporar una barra de búsqueda de texto en la cabecera del frontend.
  - [ ] Filtrar en tiempo real los ítems visibles en la grilla según el título, autor/director o notas que coincidan con la búsqueda.
  - [ ] Garantizar que el filtro de búsqueda combine de forma limpia con los filtros de categoría seleccionados.

### [ ] Botón de recomendación "Al azar"
- **Problema:** Indecisión de uso por parálisis de análisis ("no sé qué ver o leer hoy").
- **Razón / Contexto:** Ayuda al usuario a elegir de manera aleatoria un contenido de su colección.
- **Definición de Hecho (DoD):**
  - [ ] Añadir un botón con estilo claymórfico interactivo ("Al azar" / "Sorpréndeme").
  - [ ] Al hacer clic, seleccionar un elemento aleatorio respetando la categoría o filtro activo en ese momento (o de toda la base de datos si no hay filtro).
  - [ ] Abrir el modal de detalle del elemento seleccionado aleatoriamente con una animación de resalto temporal.
