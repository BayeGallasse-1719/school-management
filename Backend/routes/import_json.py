"""
Import des étudiants depuis le fichier JSON validé
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from utils.json_loader import chargement
from requetes import etudiants, classe, utilisateurs, matiere, devoir, examen

router = APIRouter(prefix="/api/v1", tags=["Import"])


def _parse_date(date_str: str):
    """Convertit une date JJ/MM/AAAA en objet date"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except Exception:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return None


@router.post("/import/json")
async def importer_json():
    """
    Charge data/data_valides.json et insère / met à jour les étudiants + notes.
    Idempotent : si le numéro existe déjà, on passe.
    """
    try:
        data = chargement()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Impossible de charger le JSON : {e}")

    inserted = 0
    skipped = 0
    errors = []

    for eleve in data:
        try:
            code = eleve.get("CODE")
            numero = eleve.get("Numero")
            nom = eleve.get("Nom")
            prenom = eleve.get("Prenom")
            date_str = eleve.get("Date_de_naissance")
            nom_classe = eleve.get("Classe")
            notes = eleve.get("Note", {})

            if not all([code, numero, nom, prenom, date_str, nom_classe]):
                skipped += 1
                continue

            date_naissance = _parse_date(date_str)
            if not date_naissance:
                errors.append(f"{numero}: date invalide ({date_str})")
                continue

            # Classe
            cl = classe.get_classe_by_nom(nom_classe)
            id_classe = cl[0] if cl else classe.ajouter_classe(nom_classe)

            # Utilisateur
            us = utilisateurs.get_user_by_code(code)
            id_user = us[0] if us else utilisateurs.ajouter_user(code)

            # Étudiant déjà présent ?
            existing = etudiants.get_etudiant_by_numero(numero)
            if existing:
                skipped += 1
                continue

            id_etu = etudiants.ajouter_etudiant(
                nom=nom,
                prenom=prenom,
                numero=numero,
                date_naissance=date_naissance,
                user_id=id_user,
                classe_id=id_classe,
                source="JSON",
            )

            # Notes
            for mat_nom, contenu in notes.items():
                mat = matiere.get_matiere_by_nom(mat_nom)
                id_mat = mat[0] if mat else matiere.ajouter_matiere(mat_nom)

                # Examen
                try:
                    note_exam = float(contenu.get("note_examen", 0))
                    examen.ajouter_examen(note_exam, id_mat, id_etu)
                except Exception:
                    pass

                # Devoirs
                for n in contenu.get("note_devoir", []):
                    try:
                        devoir.ajouter_devoir(float(n), id_mat, id_etu)
                    except Exception:
                        pass

            inserted += 1

        except Exception as e:
            errors.append(f"{eleve.get('Numero', '?')}: {str(e)}")

    return {
        "message": "Import terminé",
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors[:20],  # on limite l'affichage
        "total_in_file": len(data),
    }
