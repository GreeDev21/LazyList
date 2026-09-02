import os
import sys
import shutil
import subprocess

def run_build(mode: str = "onedir"):
    print(f"=== Iniciando compilación de LazyList (Modo: {mode}) ===")
    
    # 1. Asegurar que Tailwind CSS esté compilado y actualizado
    print("\n[1/3] Compilando Tailwind CSS...")
    try:
        subprocess.run(
            ["npx", "@tailwindcss/cli", "-i", "src/styles/input.css", "-o", "static/style.css", "--minify"],
            check=True,
            shell=True
        )
        print("CSS compilado exitosamente.")
    except Exception as e:
        print(f"Advertencia al compilar CSS con tailwindcli: {e}")
        print("Continuando con el CSS existente en static/style.css...")

    # 2. Configurar y ejecutar PyInstaller
    print("\n[2/3] Ejecutando PyInstaller...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "LazyList",
        "--noconsole",
        f"--{mode}",
        "--clean",
        "--add-data", "static;static",
        # Imports dinámicos necesarios para FastAPI, Uvicorn, SQLModel y WebView
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "sqlmodel",
        "--hidden-import", "sqlalchemy.dialects.sqlite",
        "--hidden-import", "selectolax",
        "--hidden-import", "httpx",
        "launcher.py"
    ]
    
    subprocess.run(cmd, check=True)
    
    # 3. Post-procesamiento: copiar plantilla .env.example
    print("\n[3/3] Post-procesamiento...")
    dist_dir = os.path.join("dist", "LazyList") if mode == "onedir" else "dist"
    
    if os.path.exists(".env.example") and os.path.exists(dist_dir):
        shutil.copy(".env.example", os.path.join(dist_dir, ".env.example"))
        print("Copiado .env.example a la carpeta de distribución.")
        
    print("\n=======================================================")
    print(f"¡Compilación finalizada con éxito!")
    if mode == "onedir":
        print(f"Tu aplicación portable se encuentra en: dist\\LazyList\\LazyList.exe")
    else:
        print(f"Tu ejecutable standalone se encuentra en: dist\\LazyList.exe")
    print("=======================================================\n")

if __name__ == '__main__':
    mode = "onefile" if "--onefile" in sys.argv else "onedir"
    run_build(mode)
