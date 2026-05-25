from database import connexion
from classe import afficher_classe
from utilisateurs import afficher_users

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## inserer etudiant
def ajouter_etudiant(nom, prenom, numero, date_naissance, user, classe, source):
    """Fonction pour ajouter un etudiant"""
    querry = """ INSERT INTO Etudiants(numero, nom, prenom, date_naissance, user_at, classe, source)
        (%s, %s, %s, %s, %s, %s, %s)
        RETURNING numero, nom, prenom, date_naissance, user_at, classe, source;
    """
    cursor.execute(querry, (numero, nom, prenom, date_naissance, user, classe, source))
    etudiant = cursor.fetchone()
    return etudiant

## afficher etudiants
def afficher_etudiant():
    """Afficher tout les etudiants"""
    querry = "SELECT numero, nom, prenom, date_naissance, user_at, classe, source FROM etudiants;"
    cursor.execute(querry)
    etudiant = cursor.fetchall()
    return etudiant

