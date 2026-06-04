from database import connexion
from .classe import get_classe_by_nom, ajouter_classe
from .utilisateurs import get_user_by_code, ajouter_user
from fastapi import HTTPException

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## inserer etudiant
def ajouter_etudiant(nom, prenom, numero, date_naissance, user, classe, source):
    """Fonction pour ajouter un etudiant"""

    query = """INSERT INTO etudiants (numero, nom, prenom, date_naissance, user_at, classe, source)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id_etudiant;"""
    try:
        cursor.execute(query, (numero, nom, prenom, date_naissance, user, classe, source))
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur SQL: {e}")


## rechercher etudiant par numero
def get_etudiant_by_numero(numero: str):
    """afficher etudiant par son numero"""
    try:
        querry = """SELECT id_etudiant, numero, nom, prenom, date_naissance, user_at, classe, source
            FROM etudiants WHERE numero = %s;"""
        cursor.execute(querry, (numero,))
        etudiant = cursor.fetchone()  
    except:
        etudiant = None
    return etudiant

## afficher etudiants
def afficher_etudiant():
    """Afficher tout les etudiants"""
    querry = """SELECT numero, nom, prenom, date_naissance, user_at, classe, source 
        FROM etudiants ;"""
    try:
        cursor.execute(querry)
        etudiant = cursor.fetchall()
        conn.commit()
    except:
        conn.rollback()
    return etudiant

def update_etudiant(numero, nom=None, prenom=None, date_naissance=None, user=None, classe=None, archive = None):
    """Modifier les infos d'un etudiants"""
    try:
        if nom:
            cursor.execute("UPDATE etudiants SET nom = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;",(nom, numero)) 
        if prenom:
            cursor.execute("UPDATE etudiants SET prenom = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;",(prenom, numero)) 
        if date_naissance:
            cursor.execute("UPDATE etudiants SET date_naissance = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;",(date_naissance, numero))
        if user:
            cursor.execute("UPDATE etudiants SET user_at = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;", (user, numero))
        if classe:
            cursor.execute("UPDATE etudiants SET classe = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;", (classe, numero))
        if archive:
            cursor.execute("UPDATE etudiants SET archive = %s, update_at = DEFAULT, source=DEFAULT WHERE numero = %s;", (archive, numero))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur SQL: {e}")


# recuperer les notes des devoirs
def get_note_etudiant_by_numero(numero: str):
    """Recuperer les notes des etudiants et leurs matieres d'un etudiant"""
    querry = """SELECT M.nom_matiere, N.note_devoir
            FROM NoteDevoirs N
            JOIN Matieres M ON N.matiere = M.id_matiere
            JOIN Etudiants E ON E.id_etudiant = N.etudiant
            WHERE E.numero = %s
            ORDER BY M.nom_matiere;"""
    cursor.execute(querry,(numero,))
    notes = cursor.fetchall()
    return notes
    

    