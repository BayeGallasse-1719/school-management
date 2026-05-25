from database import connexion

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## ajouter les matierers a leurs classe
def ajouter_classe_matiere(classe, matiere):
    """attribuer une matiere a une classe"""
    cursor.execute("INSERT INTO ClasseMatieres(classe, matiere) (%s, %s);",(classe, matiere))
    