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

### [ ] Géneros vacíos en cómics
- **Problema:** Los cómics guardados manualmente o por API no muestran géneros.
- **Razón / Contexto:** La entidad [`Comic`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py#L62-L73) en el backend directamente no posee un atributo `genre` o `genero` definido, a diferencia de otras entidades como `Pelicula` o `Serie`.
- **Definición de Hecho (DoD):**
  - [ ] Agregar el campo `genero: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))` en la clase `Comic` en [`entities.py`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py).
  - [ ] Ejecutar/aplicar la migración de base de datos correspondiente en SQLite para soportar la columna.
  - [ ] Adaptar el formulario de carga y la visualización del detalle en el frontend para soportar los géneros en la categoría Cómics.

### [x] Modal de detalle con datos hardcodeados
- **Problema:** El modal de detalle del ítem muestra información genérica cableada en el HTML.
- **Razón / Contexto:** En [`index.html`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/index.html#L181-L257), el modal `<dialog id="detail-dialog">` incluye datos estáticos como "Absolute Batman" y "DC Comics". Si el JS no los reemplaza correctamente para ciertos tipos de categorías, el usuario ve placeholders confusos.
- **Definición de Hecho (DoD):**
  - [x] Asegurar que el cargador del modal en [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js) limpie o reemplace el 100% de los placeholders estáticos al abrir cualquier elemento.
  - [x] Comprobar que no queden textos hardcodeados de ejemplo visibles al abrir el modal de un ítem vacío o recién creado.

### [ ] Botón para carga manual y opción masiva
- **Problema:** Se necesita poder agregar elementos uno por uno y también en lote (bulk).
- **Razón / Contexto:** Agilizar la carga inicial cuando se migran listas grandes de contenido desde otras plataformas.
- **Definición de Hecho (DoD):**
  - [ ] Diseñar y programar una interfaz (dentro del modal manual o en una vista dedicada) para pegar múltiples líneas/URLs/títulos.
  - [ ] Modificar el endpoint del backend para procesar colecciones de ítems y retornarlos de forma eficiente en un solo batch.

### [x] Eliminación de opciones NSFW
- **Problema:** Quitar las opciones y marcas NSFW de la aplicación.
- **Razón / Contexto:** Decisión de uso: no se guardará contenido adulto y se quiere evitar la visualización accidental de marcas relacionadas.
- **Definición de Hecho (DoD):**
  - [x] Remover el campo `NSFW` del modelo [`Recurso`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py) en el backend y limpiar las tablas.
  - [x] Eliminar badges, botones de filtro y estilos visuales NSFW en [`index.html`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/index.html) y [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js).

### [ ] Centrar modal y adaptar detalles por categoría
- **Problema:** El modal no se posiciona en el centro de la pantalla y la estructura de los campos no varía según la categoría del ítem.
- **Razón / Contexto:** Estética y experiencia de usuario (UX): un juego necesita ficha de "tienda/mod" mientras que un libro requiere "saga/autor".
- **Definición de Hecho (DoD):**
  - [ ] Centrar los `<dialog>` utilizando Flexbox/Grid o posicionamiento absoluto centrado en CSS [`style.css`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/style.css).
  - [ ] Implementar lógica dinámica en [`app.js`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/static/app.js) para ocultar/mostrar secciones de la ficha editorial según la categoría activa del elemento.

### [x] Logs y trazabilidad del sistema
- **Problema:** Falta de logs del servidor ante fallos o llamadas API externas.
- **Razón / Contexto:** Es crítico diagnosticar fallos silenciosos cuando las APIs de terceros (como Anilist, ComicVine, etc.) cambian de contrato o fallan.
- **Definición de Hecho (DoD):**
  - [x] Configurar el módulo `logging` nativo de Python en FastAPI.
  - [x] Añadir logs en los bloques `try/except` críticos de los clientes de APIs externas ([`src/infrastructure/api_clients`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/infrastructure/api_clients)).

### [ ] Detectar tipos de recursos (webs, playlist, artículos)
- **Problema:** Analizar si realmente vale la pena categorizar los recursos por tipo.
- **Razón / Contexto:** Nota escrita en libreta de la cual no se recuerda la motivación exacta.
- **Definición de Hecho (DoD):**
  - [ ] Definir si aporta valor clasificar un "recurso" o si con la URL y la descripción general ya es suficiente. Si se descarta, eliminar la columna `tipo` de la entidad [`Recurso`](file:///c:/Users/aguse/Desktop/Workspace/Proyectos/Web/Apps/LazyList/src/domain/entities.py#L106).

### [ ] Revisar formulario de carga manual
- **Problema:** El formulario manual es muy genérico y no permite parametrizar datos finos.
- **Razón / Contexto:** Consecuencia del ítem de géneros vacíos en cómics: si la carga manual no expone campos específicos de la categoría seleccionada, la base de datos queda incompleta.
- **Definición de Hecho (DoD):**
  - [ ] Modificar el formulario de carga manual para que al cambiar de categoría muestre u oculte inputs específicos (ej. escritor para cómics, autor para libros, url para recursos).
