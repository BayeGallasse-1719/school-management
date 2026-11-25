"""Requêtes sur la table Classes"""
from database import get_cursor
from fastapi import HTTPException


def afficher_classes() -> list:
    with get_cursor() as cur:
        cur.execute("SELECT id_classe, nom_classe FROM Classes ORDER BY nom_classe;")
        return cur.fetchall()


def get_classe_by_nom(nom: str):
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_classe, nom_classe FROM Classes WHERE LOWER(nom_classe) = LOWER(%s);",
            (nom,),
        )
        return cur.fetchone()


def get_classe_by_id(id_classe: int) -> str | None:
    with get_cursor() as cur:
        cur.execute("SELECT nom_classe FROM Classes WHERE id_classe = %s;", (id_classe,))
        row = cur.fetchone()
        return row[0] if row else None


def ajouter_classe(nom: str) -> int:
    existing = get_classe_by_nom(nom)
    if existing:
        return existing[0]

    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO Classes(nom_classe) VALUES (%s) RETURNING id_classe;",
            (nom,),
        )
        return cur.fetchone()[0]


def compter_classes() -> int:
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM Classes;")
        return cur.fetchone()[0]
