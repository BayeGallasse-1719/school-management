"""Requêtes sur NoteDevoirs"""
from database import get_cursor


def ajouter_devoir(note: float, matiere_id: int, etudiant_id: int) -> None:
    with get_cursor() as cur:
        cur.execute(
            """INSERT INTO NoteDevoirs(note_devoir, matiere, etudiant)
               VALUES (%s, %s, %s);""",
            (note, matiere_id, etudiant_id),
        )


def modifier_devoir(note: float, id_note: int) -> None:
    with get_cursor() as cur:
        cur.execute(
            """UPDATE NoteDevoirs
               SET note_devoir = %s, update_at = CURRENT_TIMESTAMP, update_note = TRUE
               WHERE id_note = %s;""",
            (note, id_note),
        )


def get_devoirs_etudiant(etudiant_id: int) -> list:
    with get_cursor() as cur:
        cur.execute(
            """SELECT nd.id_note, m.nom_matiere, nd.note_devoir
               FROM NoteDevoirs nd
               JOIN Matieres m ON m.id_matiere = nd.matiere
               WHERE nd.etudiant = %s
               ORDER BY m.nom_matiere, nd.id_note;""",
            (etudiant_id,),
        )
        return cur.fetchall()
