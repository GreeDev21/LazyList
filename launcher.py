import socket
import threading
import time
import multiprocessing
import uvicorn
import webview
from src.api.main import app

def find_free_port(start_port: int = 8000) -> int:
    """Busca el primer puerto disponible a partir de start_port."""
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1
    return start_port

class ServerThread(threading.Thread):
    """Hilo demonio para ejecutar Uvicorn en segundo plano sin bloquear el hilo de la GUI."""
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.config = uvicorn.Config(
            app=app,
            host=self.host,
            port=self.port,
            log_level="info",
            loop="asyncio",
            log_config=None
        )
        self.server = uvicorn.Server(config=self.config)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True

def main():
    multiprocessing.freeze_support()
    
    port = find_free_port(8000)
    server = ServerThread(port=port)
    server.start()

    # URL base del frontend
    url = f"http://127.0.0.1:{port}/"

    # Iniciar ventana nativa (WebView2 en Windows)
    window = webview.create_window(
        title="LazyList",
        url=url,
        width=1280,
        height=850,
        min_size=(900, 600)
    )

    # Iniciar la interfaz gráfica en modo privado (sin caché persistente) y con herramientas de inspección (F12) habilitadas
    webview.start(private_mode=True, debug=True)

    # Apagar el servidor y liberar el puerto
    server.stop()
    server.join(timeout=3)

if __name__ == '__main__':
    main()
