from database import connexion

## creer une connexionn
conn = connexion()
cursor = conn.cursor()

## ajouter une note de devoir
def ajouter_devoir(note, matiere, etudiant):
    """ajouter une note de devoir""" 
    cursor.execute("""INSERT INTO NoteDevoirs(note_devoir, matiere, etudiant) 
            (%s, %s, %s);""",(note, matiere, etudiant))
    
    
