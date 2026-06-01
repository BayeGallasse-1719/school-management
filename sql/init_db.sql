CREATE DATABASE GestionEcole;
\c GestionEcole;

##----CREATION DES TABLES
CREATE TABLE Etudiants(
    id_etudiant SERIAL NOT NULL PRIMARY KEY,
    numero VARCHAR(7) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE NOT NULL,
    user_at INTEGER NOT NULL,
    classe INTEGER NOT NULL,
    source VARCHAR(10) NOT NULL DEFAULT 'DB',
    archive BOOLEAN DEFAULT FALSE,
    update_etudiant BOOLEAN DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Matieres(
    id_matiere SERIAL NOT NULL PRIMARY KEY,
    nom_matiere VARCHAR(100) NOT NULL UNIQUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE NoteDevoirs(
    id_note SERIAL PRIMARY KEY,
    note_devoir FLOAT NOT NULL,
    CHECK(note_devoir>=0 AND note_devoir<=20),
    matiere INTEGER NOT NULL,
    etudiant INTEGER NOT NULL,
    update_note BOOLEAN DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Classes(
    id_classe SERIAL NOT NULL PRIMARY KEY,
    nom_classe VARCHAR(100) NOT NULL UNIQUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE NoteExamens(
    matiere INTEGER NOT NULL,
    etudiant INTEGER NOT NULL,
    note_examen FLOAT NOT NULL,
    CHECK(note_examen>=0 AND note_examen<=20),
    PRIMARY KEY(matiere, etudiant),
    update_examen BOOLEAN DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Utilisateurs(
    id_code SERIAL NOT NULL PRIMARY KEY,
    code VARCHAR(6) NOT NULL UNIQUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## Relations
ALTER TABLE Etudiants 
ADD FOREIGN KEY(classe) REFERENCES Classes(id_classe),
ADD FOREIGN KEY(user_at) REFERENCES Utilisateurs(id_code);

ALTER TABLE NoteDevoirs
ADD FOREIGN KEY(matiere) REFERENCES Matieres(id_matiere),
ADD FOREIGN KEY(etudiant) REFERENCES Etudiants(id_etudiant);

ALTER TABLE NoteExamens
ADD FOREIGN KEY(matiere) REFERENCES Matieres(id_matiere),
ADD FOREIGN KEY(etudiant) REFERENCES Etudiants(id_etudiant);


