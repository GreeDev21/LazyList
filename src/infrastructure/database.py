import os
from sqlmodel import SQLModel, create_engine, Session

class Database:
    def __init__(self, db_path: str = "lazylinks.db"):
        self.db_path = db_path
        # SQLite URL
        sqlite_url = f"sqlite:///{db_path}"
        # Se requiere check_same_thread=False para FastAPI en SQLite
        self.engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

    def get_session(self) -> Session:
        return Session(self.engine, expire_on_commit=False)

    def init_db(self):
        """Inicializa la base de datos creando las tablas a partir de los modelos de SQLModel"""
        SQLModel.metadata.create_all(self.engine)
