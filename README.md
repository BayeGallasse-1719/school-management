# 📊 Projet Final Intégrateur - Data Visualisation & API

**Dev Data P8** - Exploitation des données Python dans une application Web

---

## 🎯 Objectif du projet

Construire une application web professionnelle complète qui permet de :

- Afficher, gérer et visualiser des données d'étudiants
- Combiner intelligemment les données issues de **PostgreSQL** et d'un fichier **JSON**
- Proposer des fonctionnalités avancées : pagination, recherche, modification, archivage, import, dashboard statistique

---

## 🛠️ Technologies utilisées

| Catégorie | Technologies |
|-----------|--------------|
| **Backend** | Python, FastAPI, Pydantic |
| **Base de données** | PostgreSQL, SQL manuel (sans ORM) |
| **Frontend** | HTML5, CSS3, JavaScript (Fetch API) |
| **Visualisation** | Chart.js |
| **Versionnement** | Git, GitHub |
| **Environnement** | Linux, Bash |

---

## 📁 Structure du projet
mon_projet/
├── backend/
│   ├── main.py              (FastAPI)
│   ├── database.py          (connexion PostgreSQL)
│   ├── shema.py            (Pydantic)
│   ├── routes/
│   │   ├── etudiants.py      (API étudiants)
│   │   ├── dashboard.py     (API statistiques)
│   │   └── import_jons.py        (API import JSON)
│   └── utils/
│       └── json_loader.py   (chargement valides.json)
├── frontend/
│   ├── index.html           (page liste étudiants)
│   ├── dashboard.html       (page statistiques)
│   ├── css/
│   |   └──style.css
│   └── script.js            (fetch API + affichage)
├── data/
│   ├── valides.json
│   └── invalides.json (optionnel)
├── sql/
│   └── init_db.sql          (création tables)
└── README.md