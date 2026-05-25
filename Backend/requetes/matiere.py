from database import connexion

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## ajouter une matiere
def ajouter_matiere(nom):
    """ajouter une matiere"""
    cursor.execute("INSERT INTO Matieres(nom_matiere) (%s);",(nom,))