from fastapi import APIRouter, HTTPException
from requetes import etudiants, classe, utilisateurs, matiere, devoir
from shema import (EtudiantResponse, Etudiant, UpdateEtudiant, CreateEtudiant,
                   EtudiantDetailResponse, NoteResponse)

router = APIRouter()

@router.get('/api/v1/etudiants', response_model=list[EtudiantResponse], tags=['Etudiant'])
async def get_etudiant():
    """afficher tout les etudiants"""
    etudiant = etudiants.afficher_etudiant()
    return [EtudiantResponse(numero=e[0], nom=e[1], prenom=e[2], date_naissance=e[3],
                             user_at=utilisateurs.get_user_by_id(e[4]), classe=classe.get_classe_by_id(e[5]), 
                             source=e[6]) for e in etudiant]


@router.get('/api/v1/etudiants/{numero}', response_model=EtudiantDetailResponse, tags=['Etudiant'])
async def get_etudiant_num(numero:str):
    "Get student by numero"
    etudiant = etudiants.get_etudiant_by_numero(numero)
    if not etudiant:
        raise HTTPException(status_code=404, detail='Student Not Found !')
    ## Recuperer le nom de la classe
    nom_classe = classe.get_classe_by_id(etudiant[6])
    ## Recuperer le code
    code_user = utilisateurs.get_user_by_id(etudiant[5])
    ## Recuperer les notes
    notes_data = etudiants.get_note_etudiant_by_numero(numero) 
    notes = [
        NoteResponse(matiere=n[0], note=n[1])
        for n in notes_data
    ]
    return EtudiantDetailResponse(
        numero=etudiant[1],
        nom=etudiant[2],
        prenom=etudiant[3],
        date_naissance=etudiant[4],
        user_at=code_user,
        classe=nom_classe,
        source=etudiant[7],
        notes=notes
    )



@router.post('/api/v1/etudiants', tags=['Etudiant'])
async def post_etudiant(etudiant: Etudiant):
    """ajouter etudiant"""
    verif_numero = etudiants.get_etudiant_by_numero(etudiant.numero)
    id_classe = classe.get_classe_by_nom(classe=etudiant.classe)
    if id_classe is None:
        raise HTTPException(status_code=400, detail="Classe inexistante")

    id_user = utilisateurs.get_user_by_code(code=etudiant.user_at)
    if id_user is None:
        raise HTTPException(status_code=400, detail="Utilisateur inexistant")

    if verif_numero:
        raise HTTPException(status_code=403, detail="student already exists !")
    etudiant : CreateEtudiant
    etudiants.ajouter_etudiant(etudiant.nom, etudiant.prenom, etudiant.numero,
                etudiant.date_naissance, id_user[0], id_classe[0], etudiant.source)
    return {'Succee': 'Etudiant ajouter avec succee !'}
    
    
@router.patch('/api/v1/etudiants/{numero}', tags=['Etudiant'])
async def update_etudiant(numero: str, etudiant: UpdateEtudiant):
    """modifier les attributs d'un etudiant"""
    verif_numero = etudiants.get_etudiant_by_numero(numero)
    if not verif_numero:
        raise HTTPException(status_code=404, detail="student Not Found !")
    
    id_classe = classe.get_classe_by_nom(classe=etudiant.classe)
    if id_classe is None:
        raise HTTPException(status_code=400, detail="Classe inexistante")

    id_user = utilisateurs.get_user_by_code(code=etudiant.user_at)
    if id_user is None:
        raise HTTPException(status_code=400, detail="Utilisateur inexistant")
    
    etudiants.update_etudiant(numero=numero, nom=etudiant.nom, prenom=etudiant.prenom, 
                date_naissance=etudiant.date_naissance, user=id_user[0], classe=id_classe[0])

@router.post('/api/v1/etudiants/{numero}/notesDevoir', tags=['Notes'])   
async def ajouter_note_matiere(numero:str, data: NoteResponse ):
    """ajouter une note son matiere par son numero"""
    print(numero, data.note, data.matiere)
    ## verifier si l'etudiant exist
    id_numero = etudiants.get_etudiant_by_numero(numero)
    ## verifier si la matiere existe ou pas
    id_matiere = matiere.get_matiere_by_nom(data.matiere)
    if not id_matiere:
        ## sinon ajouter la matiere
        id_matiere = matiere.ajouter_matiere(data.matiere)
    devoir.ajouter_devoir(note=data.note, matiere=id_matiere[0], etudiant=id_numero[0])
    return {'Succee': 'Note Enregistrer !'}
