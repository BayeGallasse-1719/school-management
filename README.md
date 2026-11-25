# 🎓 Gestion École - Application Web Full Stack

## 📖 Présentation

Gestion École est une application web développée dans le cadre du projet final intégrateur DEV DATA P8.

L'objectif consiste à réutiliser des données académiques préalablement collectées, nettoyées, validées et exportées au format JSON afin de construire une application web complète reposant sur :

- Python
- FastAPI
- PostgreSQL
- SQL manuel
- HTML / CSS / JavaScript
- Chart.js
- Linux
- Git & GitHub

L'application permet de gérer les étudiants, consulter les notes, calculer les moyennes, importer des données JSON vers PostgreSQL et visualiser des statistiques grâce à un tableau de bord interactif.

---

## 🎯 Objectifs pédagogiques

Ce projet permet de mettre en pratique :

- Algorithmique
- Python
- Programmation Orientée Objet (POO)
- Manipulation de fichiers JSON
- SQL et PostgreSQL
- Développement d'API REST avec FastAPI
- Développement Frontend avec HTML, CSS et JavaScript
- Visualisation de données avec Chart.js
- Linux et Bash
- Gestion de version avec Git et GitHub

---

## 🏗️ Architecture

```text
                 +----------------+
                 |  valides.json  |
                 +--------+-------+
                          |
                          v
+-------------+   +---------------+   +--------------+
| Frontend    |<->| FastAPI REST  |<->| PostgreSQL   |
| HTML/CSS/JS |   | API Backend   |   | Base données |
+-------------+   +---------------+   +--------------+
                          |
                          v
                 +----------------+
                 | Dashboard      |
                 | Chart.js       |
                 +----------------+

✨ Fonctionnalités réalisées
Gestion des étudiants
✅ Consultation des étudiants
✅ Ajout d'un étudiant
✅ Modification d'un étudiant
✅ Archivage / restauration
✅ Recherche multicritères
✅ Pagination côté serveur
Gestion des données
✅ Import des données JSON
✅ Détection des doublons
✅ Fusion PostgreSQL + JSON
✅ Identification de la source des données (DB / JSON)
Gestion académique
✅ Gestion des matières
✅ Gestion des devoirs
✅ Gestion des examens
✅ Calcul des moyennes
✅ Bulletin détaillé d'un étudiant
Dashboard décisionnel
✅ Nombre total d'étudiants
✅ Répartition par classe
✅ Répartition par source
✅ Top 10 des meilleures moyennes
✅ Statistiques globales
✅ Visualisation avec Chart.js

🛠️ Stack technique
Couche	TechnologiesBackend	Python 3.12, FastAPI, Pydantic, Psycopg2
Base de données	PostgreSQL
API	REST
Frontend	HTML5, CSS3, JavaScript
Visualisation	Chart.js
Scripting	Bash
Versionning	Git / GitHub
📁 Structure du projet
Projet/
│
├── Backend/
│   ├── main.py
│   ├── database.py
│   ├── schema.py
│   ├── routes/
│   │   ├── etudiants.py
│   │   ├── import_json.py
│   │   └── dashboard.py
│   │
│   ├── requetes/
│   │   ├── etudiants.py
│   │   ├── classe.py
│   │   ├── utilisateurs.py
│   │   ├── devoir.py
│   │   ├── examen.py
│   │   └── matiere.py
│   │
│   └── utils/
│       └── json_loader.py
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── script.js
│   ├── dashboard.js
│   └── css/style.css
│
├── data/
│   ├── data_valides.json
│   └── data_invalides.json
│
├── sql/
│   └── init_db.sql
│
├── requirements.txt
├── .env
└── README.md

⚙️ Configuration

Créer un fichier .env à la racine du projet :

DB_NAME=gestioncollege
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_HOST=localhost
DB_PORT=5432

🚀 Installation
1. Cloner le projet
git clone <url-du-repository>
cd Projet

2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate

3. Installer les dépendances
pip install -r requirements.txt

4. Créer la base PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE gestioncollege;"

5. Initialiser les tables
sudo -u postgres psql \
-d gestioncollege \
-f sql/init_db.sql

6. Démarrer le backend
cd Backend
./run.sh


ou

uvicorn main:app --reload


Documentation Swagger :

http://localhost:8000/docs

7. Démarrer le frontend
cd frontend
python -m http.server 5500


Puis ouvrir :

http://localhost:5500

📡 Principales routes API
Méthode	Endpoint	DescriptionGET	/api/v1/health	Vérification API
GET	/api/v1/etudiants	Liste paginée
GET	/api/v1/etudiants/{numero}	Détail étudiant
POST	/api/v1/etudiants	Ajout
PUT	/api/v1/etudiants/{numero}	Modification
PATCH	/api/v1/etudiants/{numero}/archiver	Archivage
POST	/api/v1/import/json	Import JSON
GET	/api/v1/dashboard	Dashboard
POST	/api/v1/notes/devoir	Ajout note devoir
POST	/api/v1/notes/examen	Ajout note examen
🎓 Compétences démontrées
Développement Backend avec FastAPI
Conception de bases PostgreSQL
SQL avancé sans ORM
Développement d'API REST
Gestion des données JSON
Architecture Full Stack
Data Visualisation
Linux & Bash
Git & GitHub
Organisation modulaire d'un projet professionnel
👨‍💻 Auteur

Baye Gallasse

Étudiant en Statistiques et Informatique Décisionnelle et apprenant au programme Développement Data de l'Orange Digital Center, passionné par :

BI Analyst
Data Science
Data Engineering
Développement Backend
Architecture de données
Intelligence Artificielle
