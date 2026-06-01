from database import connexion

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## ajouter une matiere
def ajouter_matiere(nom: str):
    """ajouter une matiere"""
    cursor.execute("INSERT INTO Matieres(nom_matiere) VALUES (%s) RETURNING id_matiere;",(nom,))
    id = cursor.fetchone()
    conn.commit()
    return id[0]

def get_matiere_by_nom(nom:str):
    """afficher matiere par son nom"""
    try:
        cursor.execute("SELECT id_matiere, nom FROM Matieres WHERE nom_matiere = %s;",(nom,))
        id = cursor.fetchone()
    except:
        id = None
    return id