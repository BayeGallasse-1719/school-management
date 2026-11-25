"""
API Dashboard - Statistiques
"""
from fastapi import APIRouter
from database import get_cursor
from shema import StatsDashboard
from requetes import etudiants, classe, matiere

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])


@router.get("/dashboard", response_model=StatsDashboard)
async def get_dashboard():
    """Statistiques globales pour le dashboard"""

    total_etudiants = etudiants.compter_etudiants(archive=False)
    total_classes = classe.compter_classes()
    total_matieres = matiere.compter_matieres()

    with get_cursor(dict_cursor=True) as cur:
        # Étudiants par classe
        cur.execute(
            """
            SELECT c.nom_classe AS label, COUNT(e.id_etudiant) AS value
            FROM Classes c
            LEFT JOIN Etudiants e ON e.classe = c.id_classe AND e.archive = FALSE
            GROUP BY c.nom_classe
            ORDER BY value DESC;
            """
        )
        etudiants_par_classe = [dict(r) for r in cur.fetchall()]

        # Étudiants par source
        cur.execute(
            """
            SELECT COALESCE(source, 'DB') AS label, COUNT(*) AS value
            FROM Etudiants
            WHERE archive = FALSE
            GROUP BY source
            ORDER BY value DESC;
            """
        )
        etudiants_par_source = [dict(r) for r in cur.fetchall()]

        # Moyenne générale (sur les notes d'examen + moyenne devoirs)
        cur.execute(
            """
            WITH devoirs AS (
                SELECT etudiant, matiere, AVG(note_devoir) AS moy_devoir
                FROM NoteDevoirs
                GROUP BY etudiant, matiere
            ),
            notes AS (
                SELECT
                    COALESCE(d.moy_devoir, 0) AS moy_d,
                    COALESCE(ex.note_examen, 0) AS note_e,
                    CASE
                        WHEN d.moy_devoir IS NOT NULL AND ex.note_examen IS NOT NULL
                            THEN (d.moy_devoir + ex.note_examen) / 2
                        WHEN d.moy_devoir IS NOT NULL THEN d.moy_devoir
                        ELSE ex.note_examen
                    END AS moyenne
                FROM devoirs d
                FULL OUTER JOIN NoteExamens ex
                    ON d.etudiant = ex.etudiant AND d.matiere = ex.matiere
            )
            SELECT ROUND(AVG(moyenne)::numeric, 2) AS moyenne_generale
            FROM notes
            WHERE moyenne IS NOT NULL;
            """
        )
        row = cur.fetchone()
        moyenne_generale = float(row["moyenne_generale"]) if row and row["moyenne_generale"] else None

        # Top 10 étudiants (moyenne globale)
        cur.execute(
            """
            WITH devoirs AS (
                SELECT etudiant, matiere, AVG(note_devoir) AS moy_devoir
                FROM NoteDevoirs
                GROUP BY etudiant, matiere
            ),
            notes AS (
                SELECT
                    COALESCE(d.etudiant, ex.etudiant) AS etudiant,
                    CASE
                        WHEN d.moy_devoir IS NOT NULL AND ex.note_examen IS NOT NULL
                            THEN (d.moy_devoir + ex.note_examen) / 2
                        WHEN d.moy_devoir IS NOT NULL THEN d.moy_devoir
                        ELSE ex.note_examen
                    END AS moyenne
                FROM devoirs d
                FULL OUTER JOIN NoteExamens ex
                    ON d.etudiant = ex.etudiant AND d.matiere = ex.matiere
            ),
            moyennes AS (
                SELECT etudiant, ROUND(AVG(moyenne)::numeric, 2) AS moy
                FROM notes
                WHERE moyenne IS NOT NULL
                GROUP BY etudiant
            )
            SELECT e.numero, e.nom, e.prenom, c.nom_classe AS classe, m.moy
            FROM moyennes m
            JOIN Etudiants e ON e.id_etudiant = m.etudiant
            LEFT JOIN Classes c ON c.id_classe = e.classe
            WHERE e.archive = FALSE
            ORDER BY m.moy DESC
            LIMIT 10;
            """
        )
        top_etudiants = [dict(r) for r in cur.fetchall()]

        # Répartition des notes (tranches)
        cur.execute(
            """
            WITH all_notes AS (
                SELECT note_devoir AS note FROM NoteDevoirs
                UNION ALL
                SELECT note_examen FROM NoteExamens
            )
            SELECT
                CASE
                    WHEN note < 5 THEN '0-5'
                    WHEN note < 10 THEN '5-10'
                    WHEN note < 12 THEN '10-12'
                    WHEN note < 14 THEN '12-14'
                    WHEN note < 16 THEN '14-16'
                    ELSE '16-20'
                END AS label,
                COUNT(*) AS value
            FROM all_notes
            GROUP BY 1
            ORDER BY 1;
            """
        )
        repartition_notes = [dict(r) for r in cur.fetchall()]

    return StatsDashboard(
        total_etudiants=total_etudiants,
        total_classes=total_classes,
        total_matieres=total_matieres,
        etudiants_par_classe=etudiants_par_classe,
        etudiants_par_source=etudiants_par_source,
        moyenne_generale=moyenne_generale,
        top_etudiants=top_etudiants,
        repartition_notes=repartition_notes,
    )
