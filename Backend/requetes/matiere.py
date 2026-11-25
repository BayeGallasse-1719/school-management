"""Requêtes sur la table Matieres"""
from database import get_cursor


def afficher_matieres() -> list:
    with get_cursor() as cur:
        cur.execute("SELECT id_matiere, nom_matiere FROM Matieres ORDER BY nom_matiere;")
        return cur.fetchall()


def get_matiere_by_nom(nom: str):
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_matiere, nom_matiere FROM Matieres WHERE LOWER(nom_matiere) = LOWER(%s);",
            (nom,),
        )
        return cur.fetchone()


def get_matiere_by_id(id_matiere: int) -> str | None:
    with get_cursor() as cur:
        cur.execute("SELECT nom_matiere FROM Matieres WHERE id_matiere = %s;", (id_matiere,))
        row = cur.fetchone()
        return row[0] if row else None


def ajouter_matiere(nom: str) -> int:
    existing = get_matiere_by_nom(nom)
    if existing:
        return existing[0]

    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO Matieres(nom_matiere) VALUES (%s) RETURNING id_matiere;",
            (nom,),
        )
        return cur.fetchone()[0]


def compter_matieres() -> int:
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM Matieres;")
        return cur.fetchone()[0]
