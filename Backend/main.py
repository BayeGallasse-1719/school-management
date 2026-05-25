from fastapi import FastAPI
import json
import os
from requetes import etudiants, devoir, classe, classematiere, matiere, examen, utilisateurs

## instancier l'app fastapi
app = FastAPI(
    title='Gestion Ecole',
    description="Application de Gestion d'ecole",
    version='0.0.1'
)

## route import data json
@app.post('/api/v1/import/json')
def data_json():
    BASE_DIRS = os.path.dirname(os.path.abspath(__file__))
    with open(f'{BASE_DIRS}/Json/data_valides.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    ## liste pour la recuperation des cles
    liste_classe = []
    liste_code = []
    liste_matiere = []
    for id_etudiant, info in enumerate(data, 1):
        code = info['CODE']
        numero = info['Numero']
        clas = info['Classe']
        nom = info['Nom']
        prenom = info['Prenom']
        date_naissance = info['Date_de_naissance']

        ## recuperer l'id de la classe
        if not clas in liste_classe:
            liste_classe.append(clas)
            num_classe = len(liste_classe)
            ## ajouter dans la db
            classe.ajouter_classe(nom=clas)
        else:
            num_classe = liste_classe.index(clas)
        ## recuperer l'id du code
        if not code in liste_code:
            liste_code.append(code)
            num_code = len(liste_code)
            ## ajouter dans la db
            utilisateurs.ajouter_user(code=code)
        else:
            num_code = liste_code.index(code)
        
        ## ajouter les informations d'un etudiant
        etudiants.ajouter_etudiant(nom=nom, prenom=prenom, numero=numero, date_naissance=date_naissance,
                                    user=num_code, classe=num_classe, source='JSON')
        notes = info['Note']
        for id_matiere, mat in enumerate(notes, 1):
            ## ajouter la matiere
            if not mat in liste_matiere:
                liste_matiere.append(mat)
                ## ajouter dans le db
                matiere.ajouter_matiere(nom=mat)
            for note in matiere:
                note_examen = float(note['note_examen'])
                ## ajouter la note examen
                examen.ajouter_examen(note=note_examen, etudiant=id_etudiant, matiere=id_matiere)
                for n in note['note_devoir']:
                    ## ajouter les devoirs de chaque matiere
                    devoir.ajouter_devoir(note=n, etudiant=id_etudiant, matiere=id_matiere)
       


## route principal
@app.get('/api/v1/health')
async def health():
    return {'welcome' : 'Gestion ecole'}

## route pour voir tout les etudiants
@app.get('/api/v1/etudiants')
async def get_etudiants():
    """afficher tout les etudiants de la db"""
    liste_etudiants = etudiants.afficher_etudiant()
    for e in liste_etudiants:
        pass
    
