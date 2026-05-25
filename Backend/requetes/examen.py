from database import connexion

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## ajouter un examen
def ajouter_examen(matiere, etudiant, note):
    """Ajouter une note d'examen pour un etudiant dans une matiere"""
    cursor.execute("""INSERT INTO NoteExamens(matiere, etudiant, note_examen) 
            (%s, %s, %s);"""(matiere, etudiant, note))
