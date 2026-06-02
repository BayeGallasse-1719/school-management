from fastapi import APIRouter
from requetes import etudiants, devoir, classe, matiere, examen, utilisateurs
from utils import json_loader

## creer les routes
router = APIRouter()

## chargement du fichier json
@router.post('/api/v1/import/json', tags=['JSON'])
async def load_json():
    """Route chargement des donnees valides du fichier json"""
    data = json_loader.chargement()

    for eleve in data:
        code = eleve['CODE']
        numero = eleve['Numero']
        nom_classe = eleve['Classe']
        nom = eleve['Nom']
        prenom = eleve['Prenom']
        date_naissance = eleve['Date_de_naissance']

        ## verifier si la classe existe
        verif_classe = classe.get_classe_by_nom(classe=nom_classe)
        if verif_classe:
            id_classe = verif_classe[0]
        else:
            ## ajouter dans la db
            id_classe = classe.ajouter_classe(nom=nom_classe)
        
        ## verifier si le code existe
        verif_code = utilisateurs.get_user_by_code(code=code)
        if verif_code:
            id_code = verif_code[0]
        else:
            ## ajouter dans la db
            id_code = utilisateurs.ajouter_user(code=code)

        ## verifier si le numero n'existe pas 
        verif_numero = etudiants.get_etudiant_by_numero(numero=numero)
        if verif_numero:
            id_etudiant = verif_numero[0]
            continue
        else:
            ## ajouter les infos d'un etudiant
            id_etudiant = etudiants.ajouter_etudiant(nom=nom, prenom=prenom, numero=numero, date_naissance=date_naissance,
                                    user=id_code, classe=id_classe, source='JSON')
            
            notes = eleve['Note']
            for mat, contenu in notes.items():
                ## verifier si la matiere existe
                verif_matiere = matiere.get_matiere_by_nom(nom=mat)
                if verif_matiere:
                    id_matiere = verif_matiere[0]
                else:
                    ## ajouter dans le db
                    id_matiere = matiere.ajouter_matiere(nom=mat)

                note_examen = float(contenu['note_examen'])
                ## ajouter la note examen
                examen.ajouter_examen(note=note_examen, etudiant=id_etudiant, matiere=id_matiere)
                for n in contenu['note_devoir']:
                    ## ajouter les devoirs de chaque matiere
                    devoir.ajouter_devoir(note=n, etudiant=id_etudiant, matiere=id_matiere)

    