# Guía: ¿Cómo leer e interpretar los logs del sistema?

Este documento explica cómo está estructurado el sistema de logs de **LazyList** y cómo utilizarlos para diagnosticar el comportamiento de la aplicación y resolver errores de integración con servicios externos.

---

## 📋 1. Estructura Básica de un Log

Cada línea de log generada por la aplicación sigue un patrón unificado:

```text
[Timestamp] - [Logger] - [Level] - [Message]
```

### Componentes:
1. **Timestamp** (`2026-08-23 19:45:54,183`): Fecha y hora exacta con milisegundos en la que ocurrió el evento.
2. **Logger** (`lazylist` u `httpx`): El nombre del módulo que generó el log. 
   - `lazylist`: Logs de nuestra propia lógica de negocio y controladores.
   - `httpx`: Logs del cliente HTTP que realiza las peticiones a APIs externas.
3. **Level** (`INFO`, `ERROR`, `WARNING`): Gravedad o tipo del evento.
4. **Message**: La descripción detallada del suceso.

---

## 🪵 2. Niveles de Log en el Sistema

### 🔹 INFO (Operaciones Normales)
Se utiliza para registrar el flujo regular de la aplicación (búsquedas iniciadas, guardados exitosos y peticiones HTTP completadas).
*Ejemplo:*
```text
2026-08-23 19:45:54,183 - lazylist - INFO - Iniciando búsqueda externa: query='...', categoria='recursos'
```

### 🔸 ERROR (Fallos y Excepciones)
Se dispara cuando ocurre una excepción inesperada (por ejemplo, timeout en una API de terceros, caída de internet, o cambios de contrato en servicios como TMDB o AniList). Incluye siempre la traza de ejecución o **Traceback** de Python.
*Ejemplo:*
```text
2026-08-23 19:50:19,505 - lazylist - ERROR - Error en la búsqueda externa para la categoría 'peliculas' ...
```

---

## 🔍 3. Cómo leer un Traceback de Error

Cuando ocurre un error, el log imprime la traza completa desde dónde se originó hasta dónde se capturó. Para analizarlo eficientemente:

1. **El Mensaje Inicial del Logger**:
   ```text
   2026-08-23 19:50:19,505 - lazylist - ERROR - Error en la búsqueda externa para la categoría 'peliculas' con query 'transformers': [Errno 11001] getaddrinfo failed
   ```
   Aquí ves de inmediato qué categoría falló y el error crudo del sistema (`getaddrinfo failed`, que usualmente indica falta de conexión o resolución de DNS).

2. **La Traza de Causa Directa (Bottom-up)**:
   Los tracebacks de Python se leen de arriba a abajo, siendo la última línea el error definitivo y el módulo en el que ocurrió.
   ```text
   File "C:\Users\aguse\Desktop\Workspace\Proyectos\Web\Apps\LazyList\src\infrastructure\api_clients\router_client.py", line 59, in search
     results = client.search(query, category)
   ```
   Esta sección te muestra exactamente en qué línea de nuestro código (`router_client.py`, función `search`) se interceptó y detuvo el flujo.

3. **El Error Definitivo**:
   ```text
   httpx.ConnectError: [Errno 11001] getaddrinfo failed
   ```
   Muestra el tipo de excepción final. En este caso, un error de conexión (`ConnectError`) al intentar pegarle al endpoint externo.

---

## ⚙️ 4. Logs de Aplicación vs. Logs de Uvicorn

En la consola de desarrollo vas a ver convivir dos tipos de salidas:
1. **Logs de LazyList** (tienen el formato con timestamp detallado):
   ```text
   2026-08-23 19:46:11,457 - lazylist - INFO - Búsqueda externa completada con éxito. Resultados: 1
   ```
2. **Logs del Servidor Uvicorn** (tienen formato simple con prefijo `INFO:`):
   ```text
   INFO:     127.0.0.1:59218 - "GET /api/search?q=... HTTP/1.1" 200 OK
   ```
   Estos últimos registran la petición HTTP entrante que hace tu navegador al backend de FastAPI y el código de estado HTTP retornado (ej: `200 OK` o `500 Internal Server Error`).
