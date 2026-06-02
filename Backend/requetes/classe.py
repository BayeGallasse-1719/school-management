from database import connexion
from fastapi import HTTPException

conn = connexion()
cursor = conn.cursor()

def afficher_classe():
    """afficher tout les classes"""
    cursor.execute("SELECT id_classe, nom_classe FROM Classes;")
    classes = cursor.fetchall()
    conn.close()
    return classes

def ajouter_classe(nom):
    """ajouter une classe"""
    try:
        # verifier si le nom de la classe existe
        cursor.execute("SELECT nom_classe FROM Classes WHERE LOWER(nom_classe) = %s", (nom.lower(),))
        if cursor.fetchone():
            raise HTTPException(status_code=403, detail='Classe already exist !')
        cursor.execute("INSERT INTO Classes(nom_classe) VALUES (%s) RETURNING id_classe;",(nom,))
        id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id
    except:
        return None

def get_classe_by_nom(classe: str):
    """afficher la classe par son nom"""  
    try:
        cursor.execute("SELECT id_classe, nom_classe FROM Classes WHERE nom_classe = %s;",(classe,)) 
        id = cursor.fetchone()
    except:
        id = None
    return id

def get_classe_by_id(id:int):
    """afficher la classe par son id"""
    cursor.execute("SELECT nom_classe FROM Classes WHERE id_classe = %s;",(id,)) 
    nom = cursor.fetchone()[0]
    return nom
        
    