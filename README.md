# 🎓 Gestion École - Application Full Stack

**Projet Final Intégrateur - Data Visualisation & API**  

---

## 🎯 Objectif

Application web complète permettant de :

- Gérer les étudiants (CRUD, archivage, recherche, pagination)
- Importer des données depuis un fichier JSON validé
- Visualiser des statistiques avancées (Dashboard + Chart.js)
- Combiner données PostgreSQL + JSON

---

## 🛠️ Stack technique

| Couche       | Technologies                          |
|--------------|---------------------------------------|
| Backend      | Python 3.12, FastAPI, Pydantic, SQL manuel |
| Base de données | PostgreSQL                          |
| Frontend     | HTML5, CSS3 moderne, JavaScript (Fetch) |
| Visualisation| Chart.js 4                            |

---

## 📁 Structure

```
Projet_complet/
├── Backend/
│   ├── main.py
│   ├── database.py          # Context managers (connexions propres)
│   ├── shema.py             # Pydantic models
│   ├── requirement.txt
│   ├── routes/
│   │   ├── etudiants.py
│   │   ├── import_json.py
│   │   └── dashboard.py
│   ├── requetes/
│   │   ├── etudiants.py
│   │   ├── classe.py
│   │   ├── utilisateurs.py
│   │   ├── matiere.py
│   │   ├── devoir.py
│   │   └── examen.py
│   └── utils/
│       └── json_loader.py
├── frontend/
│   ├── index.html           # Liste + détail + CRUD
│   ├── dashboard.html       # Stats + graphiques
│   ├── script.js
│   ├── dashboard.js
│   └── css/style.css
├── data/
│   ├── data_valides.json
│   └── data_invalides.json
├── sql/
│   └── init_db.sql
└── README.md
```

---

## 🚀 Installation & Lancement

### 1. Base de données

```bash
# Créer la base
sudo -u postgres psql -c "CREATE DATABASE gestioncollege;"

# Initialiser les tables
sudo -u postgres psql -d gestioncollege -f sql/init_db.sql
```


### 2. Backend

```bash
cd Backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirement.txt

# Lancer
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Documentation interactive : http://127.0.0.1:8000/docs

### 3. Frontend

Ouvrir `frontend/index.html` avec un serveur local (recommandé) :

```bash
# Depuis la racine Projet_complet
cd frontend
python -m http.server 5500
```

Puis aller sur http://127.0.0.1:5500

Ou simplement ouvrir les fichiers HTML (CORS est configuré en `*`).

### 4. Importer les données JSON

Une fois le backend lancé, cliquer sur **Import JSON** dans l'interface  
ou appeler :

```bash
curl -X POST http://127.0.0.1:8000/api/v1/import/json
```

---

## 📡 Principales routes API

| Méthode | Endpoint                        | Description                    |
|---------|---------------------------------|--------------------------------|
| GET     | `/api/v1/health`                | Santé de l'API + DB            |
| GET     | `/api/v1/etudiants`             | Liste paginée + filtres        |
| GET     | `/api/v1/etudiants/{numero}`    | Détail + notes                 |
| POST    | `/api/v1/etudiants`             | Création                       |
| PUT     | `/api/v1/etudiants/{numero}`    | Mise à jour                    |
| PATCH   | `/api/v1/etudiants/{numero}/archiver` | Archiver / restaurer    |
| POST    | `/api/v1/import/json`           | Import fichier JSON            |
| GET     | `/api/v1/dashboard`             | Statistiques                   |
| POST    | `/api/v1/notes/devoir`          | Ajouter note devoir            |
| POST    | `/api/v1/notes/examen`          | Ajouter note examen            |

**Query params** pour la liste :  
`page`, `limit`, `search`, `classe`, `source`, `archive`

---

## ✨ Fonctionnalités livrées

- ✅ Connexions PostgreSQL robustes (context managers)
- ✅ CRUD complet étudiants
- ✅ Archivage / restauration
- ✅ Recherche + filtres (classe, source, archivés)
- ✅ Pagination côté serveur
- ✅ Import JSON idempotent
- ✅ Bulletin de notes détaillé (devoirs + examen + moyenne)
- ✅ Dashboard avec 3 graphiques Chart.js + Top 10
- ✅ Design moderne (sidebar, cards, badges, toasts, modal)
- ✅ Responsive

---
