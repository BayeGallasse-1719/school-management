-- ============================================================
-- Gestion École - Script d'initialisation PostgreSQL
-- ============================================================

DROP TABLE IF EXISTS NoteDevoirs CASCADE;
DROP TABLE IF EXISTS NoteExamens CASCADE;
DROP TABLE IF EXISTS Etudiants CASCADE;
DROP TABLE IF EXISTS Matieres CASCADE;
DROP TABLE IF EXISTS Classes CASCADE;
DROP TABLE IF EXISTS Utilisateurs CASCADE;

CREATE TABLE Utilisateurs (
    id_code     SERIAL PRIMARY KEY,
    code        VARCHAR(6)  NOT NULL UNIQUE,
    create_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    update_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Classes (
    id_classe   SERIAL PRIMARY KEY,
    nom_classe  VARCHAR(100) NOT NULL UNIQUE,
    create_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    update_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Matieres (
    id_matiere  SERIAL PRIMARY KEY,
    nom_matiere VARCHAR(100) NOT NULL UNIQUE,
    create_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    update_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Etudiants (
    id_etudiant     SERIAL PRIMARY KEY,
    numero          VARCHAR(7)  NOT NULL UNIQUE,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100) NOT NULL,
    date_naissance  DATE        NOT NULL,
    user_at         INTEGER     NOT NULL REFERENCES Utilisateurs(id_code),
    classe          INTEGER     NOT NULL REFERENCES Classes(id_classe),
    source          VARCHAR(10) NOT NULL DEFAULT 'DB',
    archive         BOOLEAN     DEFAULT FALSE,
    update_etudiant BOOLEAN     DEFAULT FALSE,
    create_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    update_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE NoteDevoirs (
    id_note     SERIAL PRIMARY KEY,
    note_devoir FLOAT   NOT NULL CHECK (note_devoir >= 0 AND note_devoir <= 20),
    matiere     INTEGER NOT NULL REFERENCES Matieres(id_matiere),
    etudiant    INTEGER NOT NULL REFERENCES Etudiants(id_etudiant),
    update_note BOOLEAN DEFAULT FALSE,
    create_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE NoteExamens (
    matiere      INTEGER NOT NULL REFERENCES Matieres(id_matiere),
    etudiant     INTEGER NOT NULL REFERENCES Etudiants(id_etudiant),
    note_examen  FLOAT   NOT NULL CHECK (note_examen >= 0 AND note_examen <= 20),
    update_examen BOOLEAN DEFAULT FALSE,
    create_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (matiere, etudiant)
);

CREATE INDEX idx_etudiants_archive ON Etudiants(archive);
CREATE INDEX idx_etudiants_classe  ON Etudiants(classe);
CREATE INDEX idx_etudiants_nom     ON Etudiants(nom, prenom);
CREATE INDEX idx_notedevoirs_etu   ON NoteDevoirs(etudiant);
CREATE INDEX idx_noteexamens_etu   ON NoteExamens(etudiant);

SELECT 'Base de données GestionÉcole initialisée avec succès.' AS status;
