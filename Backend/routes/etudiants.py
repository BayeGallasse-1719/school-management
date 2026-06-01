from fastapi import APIRouter, HTTPException
from requetes import etudiants
from shema import EtudiantResponse, Etudiant, UpdateEtudiant

router = APIRouter()

@router.get('/api/v1/etudiants', response_model=list[EtudiantResponse], tags=['Etudiant'])
async def get_etudiant():
    """afficher tout les etudiants"""
    etudiant = etudiants.afficher_etudiant()
    return [EtudiantResponse(numero=e[0], nom=e[1], prenom=e[2], date_naissance=e[3],
                             user_at=e[4], classe=e[5], source=e[6], archive=e[7])
                             for e in etudiant]


@router.get('/api/v1/etudiants/{numero}', response_model=EtudiantResponse, tags=['Etudiant'])
async def get_etudiant_num(numero:str):
    "Get student by numero"
    etudiant = etudiants.get_etudiant_by_numero(numero)
    if not etudiant:
        raise HTTPException(status_code=404, detail='Student Not Found !')
    return EtudiantResponse(numero=etudiant[0], nom=etudiant[1], prenom=etudiant[2],
                            date_naissance=etudiant[3], user_at=etudiant[4], classe=etudiant[5],
                            source=etudiant[6], archive=etudiant[7])



@router.post('/api/v1/etudiants', tags=['Etudiant'])
async def post_etudiant(etudiant: Etudiant):
    """ajouter etudiant"""
    verif_numero = etudiants.get_etudiant_by_numero(etudiant.numero)
    if verif_numero:
        raise HTTPException(status_code=401, detail="student already exists !")
    etudiants.ajouter_etudiant(etudiant.nom, etudiant.prenom, etudiant.numero,
                etudiant.date_naissance, etudiant.user_at, etudiant.classe, etudiant.source)
    return {'Succee': 'Etudiant ajouter avec succee !'}
    
    
@router.patch('/api/v1/etudiants/{numero}', tags=['Etudiant'])
async def update_etudiant(numero, etudiant: UpdateEtudiant):
    """modifier les attributs d'un etudiant"""
    etudiants.update_etudiant(numero=numero, nom=etudiant.nom, prenom=etudiant.prenom, 
                              date_naissance=etudiant.date_naissance,
                              user=etudiant.user_at, classe=etudiant.classe, source=etudiant.source)
    