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
    cursor.execute("INSERT INTO Classes(nom_classe) VALUES (%s) RETURNING id_classe;",(nom,))
    id = cursor.fetchone()[0]
    conn.commit()
    return id

def get_classe_by_nom(classe: str):
    """afficher la classe par son nom"""  
    try:
        cursor.execute("SELECT id_classe, nom_classe FROM Classes WHERE nom_classe = %s;",(classe,)) 
        id = cursor.fetchone()
    except:
        id = None
    return id

        
    