"""Requêtes sur la table Utilisateurs"""
from database import get_cursor


def afficher_users() -> list:
    with get_cursor() as cur:
        cur.execute("SELECT id_code, code FROM Utilisateurs ORDER BY code;")
        return cur.fetchall()


def get_user_by_code(code: str):
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_code, code FROM Utilisateurs WHERE code = %s;",
            (code,),
        )
        return cur.fetchone()


def get_user_by_id(id_code: int) -> str | None:
    with get_cursor() as cur:
        cur.execute("SELECT code FROM Utilisateurs WHERE id_code = %s;", (id_code,))
        row = cur.fetchone()
        return row[0] if row else None


def ajouter_user(code: str) -> int:
    existing = get_user_by_code(code)
    if existing:
        return existing[0]

    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO Utilisateurs(code) VALUES (%s) RETURNING id_code;",
            (code,),
        )
        return cur.fetchone()[0]
