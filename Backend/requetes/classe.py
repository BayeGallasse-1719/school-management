from database import connexion

conn = connexion()
cursor = conn.cursor()

def afficher_classe():
    """afficher tout les classes"""
    cursor.execute("SELECT id_classe, nom_classe FROM Classes;")
    classes = cursor.fetchall()
    return classes

def ajouter_classe(nom):
    """ajouter une classe"""
    cursor.execute("INSERT INTO Classes(nom) (%s);",(nom,))

        
    