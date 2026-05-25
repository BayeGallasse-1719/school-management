from database import connexion

conn = connexion()
cursor = conn.cursor()

def afficher_users():
    """afficher tout les utilisateurs"""
    cursor.execute("SELECT id_code, code FROM Utilisateurs;")
    users = cursor.fetchall()
    return users

def ajouter_user(code):
    """ajouter un utilisateur"""
    cursor.execute("INSERT INTO Utilisateurs(code) (%s);",(code,))

    