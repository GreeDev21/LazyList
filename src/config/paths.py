import os
import sys

def get_app_dir() -> str:
    """
    Retorna la ruta base donde residen el código y los recursos estáticos.
    - En modo empaquetado (PyInstaller): sys._MEIPASS (carpeta de extracción o bundle).
    - En modo desarrollo: la raíz del repositorio.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return getattr(sys, "_MEIPASS")
    # Dos niveles arriba de src/config -> raíz del proyecto
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_data_dir() -> str:
    """
    Retorna la ruta base donde deben persistir los datos de usuario y configuraciones locales (.db, .env).
    - En modo empaquetado (PyInstaller): la carpeta física donde reside el ejecutable (.exe).
    - En modo desarrollo: la raíz del repositorio.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Rutas canónicas del sistema
APP_DIR = get_app_dir()
DATA_DIR = get_data_dir()

STATIC_DIR = os.path.join(APP_DIR, "static")
ENV_PATH = os.path.join(DATA_DIR, ".env")
DB_PATH = os.path.join(DATA_DIR, "lazylinks.db")
LOG_PATH = os.path.join(DATA_DIR, "lazylist.log")
