from fastapi import APIRouter, HTTPException
from requetes import etudiants, classe, utilisateurs
from shema import EtudiantResponse, Etudiant, UpdateEtudiant, CreateEtudiant

router = APIRouter()

@router.get('/api/v1/etudiants', response_model=list[EtudiantResponse], tags=['Etudiant'])
async def get_etudiant():
    """afficher tout les etudiants"""
    etudiant = etudiants.afficher_etudiant()
    return [EtudiantResponse(numero=e[0], nom=e[1], prenom=e[2], date_naissance=e[3],
                             user_at=utilisateurs.get_user_by_id(e[4]), classe=classe.get_classe_by_id(e[5]), 
                             source=e[6]) for e in etudiant]


@router.get('/api/v1/etudiants/{numero}', response_model=EtudiantResponse, tags=['Etudiant'])
async def get_etudiant_num(numero:str):
    "Get student by numero"
    etudiant = etudiants.get_etudiant_by_numero(numero)
    if not etudiant:
        raise HTTPException(status_code=404, detail='Student Not Found !')
    ## Recuperer le nom de la classe
    nom_classe = classe.get_classe_by_id(etudiant[5])
    ## Recuperer le code
    code = utilisateurs.get_user_by_id(etudiant[4])
    return EtudiantResponse(numero=etudiant[0], nom=etudiant[1], prenom=etudiant[2],
                            date_naissance=etudiant[3], user_at=code, classe=nom_classe,
                            source=etudiant[6])



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
async def update_etudiant(numero, etudiant: UpdateEtudiant):
    """modifier les attributs d'un etudiant"""
    etudiants.update_etudiant(numero=numero, nom=etudiant.nom, prenom=etudiant.prenom, 
                              date_naissance=etudiant.date_naissance,
                              user=etudiant.user_at, classe=etudiant.classe, source=etudiant.source)
    