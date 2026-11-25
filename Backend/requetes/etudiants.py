"""
Requêtes principales sur les étudiants
Inclut : liste, détail, création, mise à jour, archivage, notes agrégées
"""
from database import get_cursor
from fastapi import HTTPException
from typing import Optional, List, Tuple
import math


def afficher_etudiants(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    classe: Optional[str] = None,
    source: Optional[str] = None,
    archive: bool = False,
) -> Tuple[List[tuple], int]:
    """
    Retourne (liste des étudiants, total)
    avec pagination et filtres.
    """
    conditions = ["e.archive = %s"]
    params: list = [archive]

    if search:
        conditions.append(
            "(e.numero ILIKE %s OR e.nom ILIKE %s OR e.prenom ILIKE %s)"
        )
        like = f"%{search}%"
        params.extend([like, like, like])

    if classe:
        conditions.append("c.nom_classe ILIKE %s")
        params.append(f"%{classe}%")

    if source:
        conditions.append("e.source = %s")
        params.append(source)

    where = " AND ".join(conditions)

    # Total
    count_sql = f"""
        SELECT COUNT(*)
        FROM Etudiants e
        LEFT JOIN Classes c ON c.id_classe = e.classe
        WHERE {where}
    """

    # Data
    offset = (page - 1) * limit
    data_sql = f"""
        SELECT e.numero, e.nom, e.prenom, e.date_naissance,
               u.code AS user_at, c.nom_classe AS classe, e.source, e.archive
        FROM Etudiants e
        LEFT JOIN Classes c ON c.id_classe = e.classe
        LEFT JOIN Utilisateurs u ON u.id_code = e.user_at
        WHERE {where}
        ORDER BY e.nom, e.prenom
        LIMIT %s OFFSET %s
    """

    with get_cursor() as cur:
        cur.execute(count_sql, params)
        total = cur.fetchone()[0]

        cur.execute(data_sql, params + [limit, offset])
        rows = cur.fetchall()

    return rows, total


def get_etudiant_by_numero(numero: str):
    """Retourne la ligne complète de l'étudiant (tuple)"""
    with get_cursor() as cur:
        cur.execute(
            """SELECT id_etudiant, numero, nom, prenom, date_naissance,
                      user_at, classe, source, archive
               FROM Etudiants WHERE numero = %s;""",
            (numero,),
        )
        return cur.fetchone()


def ajouter_etudiant(
    nom: str,
    prenom: str,
    numero: str,
    date_naissance,
    user_id: int,
    classe_id: int,
    source: str = "DB",
) -> int:
    with get_cursor() as cur:
        cur.execute(
            """INSERT INTO Etudiants(numero, nom, prenom, date_naissance, user_at, classe, source)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id_etudiant;""",
            (numero, nom, prenom, date_naissance, user_id, classe_id, source),
        )
        return cur.fetchone()[0]


def update_etudiant(
    numero: str,
    nom: Optional[str] = None,
    prenom: Optional[str] = None,
    date_naissance=None,
    user_id: Optional[int] = None,
    classe_id: Optional[int] = None,
    archive: Optional[bool] = None,
) -> None:
    sets = []
    params = []

    if nom is not None:
        sets.append("nom = %s")
        params.append(nom)
    if prenom is not None:
        sets.append("prenom = %s")
        params.append(prenom)
    if date_naissance is not None:
        sets.append("date_naissance = %s")
        params.append(date_naissance)
    if user_id is not None:
        sets.append("user_at = %s")
        params.append(user_id)
    if classe_id is not None:
        sets.append("classe = %s")
        params.append(classe_id)
    if archive is not None:
        sets.append("archive = %s")
        params.append(archive)

    if not sets:
        return

    sets.append("update_at = CURRENT_TIMESTAMP")
    sets.append("update_etudiant = TRUE")
    sets.append("source = 'DB'")  # après modification manuelle

    sql = f"UPDATE Etudiants SET {', '.join(sets)} WHERE numero = %s;"
    params.append(numero)

    with get_cursor() as cur:
        cur.execute(sql, params)
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")


def archiver_etudiant(numero: str, archive: bool = True) -> None:
    update_etudiant(numero, archive=archive)


def get_notes_detaillees(numero: str) -> list:
    """
    Retourne pour un étudiant une structure propre :
    [{matiere, note_devoirs: [...], note_examen, moyenne}, ...]
    """
    etudiant = get_etudiant_by_numero(numero)
    if not etudiant:
        return []

    etudiant_id = etudiant[0]

    with get_cursor() as cur:
        # Toutes les matières qui ont au moins une note pour cet étudiant
        cur.execute(
            """
            SELECT DISTINCT m.id_matiere, m.nom_matiere
            FROM Matieres m
            WHERE m.id_matiere IN (
                SELECT matiere FROM NoteDevoirs WHERE etudiant = %s
                UNION
                SELECT matiere FROM NoteExamens WHERE etudiant = %s
            )
            ORDER BY m.nom_matiere;
            """,
            (etudiant_id, etudiant_id),
        )
        matieres = cur.fetchall()

        result = []
        for mid, mnom in matieres:
            # Devoirs
            cur.execute(
                """SELECT note_devoir FROM NoteDevoirs
                   WHERE etudiant = %s AND matiere = %s
                   ORDER BY id_note;""",
                (etudiant_id, mid),
            )
            devoirs = [r[0] for r in cur.fetchall()]

            # Examen
            cur.execute(
                """SELECT note_examen FROM NoteExamens
                   WHERE etudiant = %s AND matiere = %s;""",
                (etudiant_id, mid),
            )
            exam_row = cur.fetchone()
            note_examen = exam_row[0] if exam_row else None

            # Moyenne (même formule que dans le JSON d'origine)
            moyenne = None
            if devoirs and note_examen is not None:
                moy_devoir = sum(devoirs) / len(devoirs)
                moyenne = round((moy_devoir + note_examen) / 2, 3)
            elif devoirs:
                moyenne = round(sum(devoirs) / len(devoirs), 3)
            elif note_examen is not None:
                moyenne = note_examen

            result.append(
                {
                    "matiere": mnom,
                    "note_devoirs": devoirs,
                    "note_examen": note_examen,
                    "moyenne": moyenne,
                }
            )

    return result


def compter_etudiants(archive: bool = False) -> int:
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM Etudiants WHERE archive = %s;", (archive,))
        return cur.fetchone()[0]
