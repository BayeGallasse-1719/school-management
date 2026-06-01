import json
import os

def chargement():
    """chargement des donnees valides et retourne une liste de dictionnaire"""
    BASE_DIRS = os.path.dirname(os.path.abspath(__file__))
    ## le dossier ou se trouve le fichier
    projet_dir = os.path.dirname(os.path.dirname(BASE_DIRS))
    ## chemin du fichier
    json_path = os.path.join(projet_dir, 'data', 'data_valides.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data