"""Requêtes sur NoteExamens"""
from database import get_cursor


def ajouter_examen(note: float, matiere_id: int, etudiant_id: int) -> None:
    with get_cursor() as cur:
        # ON CONFLICT pour éviter les doublons 
        cur.execute(
            """INSERT INTO NoteExamens(matiere, etudiant, note_examen)
               VALUES (%s, %s, %s)
               ON CONFLICT (matiere, etudiant)
               DO UPDATE SET note_examen = EXCLUDED.note_examen,
                             update_at = CURRENT_TIMESTAMP,
                             update_examen = TRUE;""",
            (matiere_id, etudiant_id, note),
        )


def modifier_examen(note: float, matiere_id: int, etudiant_id: int) -> None:
    with get_cursor() as cur:
        cur.execute(
            """UPDATE NoteExamens
               SET note_examen = %s, update_at = CURRENT_TIMESTAMP, update_examen = TRUE
               WHERE matiere = %s AND etudiant = %s;""",
            (note, matiere_id, etudiant_id),
        )


def get_examens_etudiant(etudiant_id: int) -> list:
    with get_cursor() as cur:
        cur.execute(
            """SELECT m.nom_matiere, ne.note_examen
               FROM NoteExamens ne
               JOIN Matieres m ON m.id_matiere = ne.matiere
               WHERE ne.etudiant = %s
               ORDER BY m.nom_matiere;""",
            (etudiant_id,),
        )
        return cur.fetchall()
