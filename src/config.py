"""Configuração de conexão com o PostgreSQL (valores padrão = docker-compose.yml)."""
import os
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER", "iot")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iot_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "iotdb")


def get_engine():
    """Cria o engine do SQLAlchemy."""
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)
