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
    cursor.execute("INSERT INTO Utilisateurs(code) VALUES (%s) RETURNING id_code;",(code,))
    id = cursor.fetchone()[0]
    conn.commit()
    return id

def get_user_by_code(code: str):
    """afficher l'utilisateur par son code"""
    try:
        cursor.execute("SELECT id_code, code FROM Utilisateurs WHERE code = %s;", (code,))
        id = cursor.fetchone()
    except:
        id = None
    return id

    