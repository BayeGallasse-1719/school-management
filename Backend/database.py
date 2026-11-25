"""
Gestion robuste de la connexion PostgreSQL
Utilisation de context manager pour éviter les fuites de connexion
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator
import os

import os
from pathlib import Path
from dotenv import load_dotenv

# Remonte jusqu'à la racine du projet
BASE_DIR = Path(__file__).resolve().parents[1]

# Charge le .env
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


@contextmanager
def get_connection() -> Generator:
    """Context manager pour obtenir une connexion propre"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


@contextmanager
def get_cursor(dict_cursor: bool = False) -> Generator:
    """
    Context manager pour obtenir un curseur.
    dict_cursor=True → retourne des RealDictCursor (pratique pour les stats)
    """
    with get_connection() as conn:
        cursor_factory = RealDictCursor if dict_cursor else None
        cursor = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


def test_connection() -> bool:
    """Test rapide de la connexion"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return True
    except Exception as e:
        print(f"[DB] Erreur de connexion : {e}")
        return False
