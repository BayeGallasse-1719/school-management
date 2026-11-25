"""Chargement du fichier JSON de données valides"""
import json
import os


def chargement() -> list:
    """Retourne la liste des étudiants valides depuis data/data_valides.json"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projet_dir = os.path.dirname(os.path.dirname(base_dir))
    json_path = os.path.join(projet_dir, "data", "data_valides.json")

    if not os.path.exists(json_path):
        # fallback relatif
        json_path = os.path.join(os.path.dirname(base_dir), "..", "data", "data_valides.json")
        json_path = os.path.abspath(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
