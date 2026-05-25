from Backend.database import connexion

conn = connexion()

if conn:
    try:
        cursor = conn.cursor()
        ## creer la table etudiant
        cursor.execute("""CREATE TABLE Etudiants(
            id_etudiant SERIAL NOT NULL PRIMARY KEY,
            numero VARCHAR(7) NOT NULL UNIQUE,
            prenom VARCHAR(100) NOT NULL,
            date_naissance DATE NOT NULL,
            user_at INTEGER NOT NULL,
            classe INTEGER NOT NULL,
            source VARCHAR(10) NOT NULL DEFAULT 'DB',
            archive BOOLEAN DEFAULT FALSE,
            update_etudiant BOOLEAN DEFAULT FALSE,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table matiere
        cursor.execute("""CREATE TABLE Matieres(
            id_matiere SERIAL NOT NULL PRIMARY KEY,
            nom_matiere VARCHAR(100) NOT NULL,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table notedevoir
        cursor.execute("""CREATE TABLE NoteDevoirs(
            id_note SERIAL PRIMARY KEY,
            note_devoir FLOAT NOT NULL,
            CHECK(note_devoir>=0 AND note_devoir<=20),
            matiere INTEGER NOT NULL,
            etudiant INTEGER NOT NULL,
            update_note BOOLEAN DEFAULT FALSE,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table classe
        cursor.execute("""CREATE TABLE Classes(
            id_classe SERIAL NOT NULL PRIMARY KEY,
            nom_classe VARCHAR(100) NOT NULL,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table classematiere
        cursor.execute("""CREATE TABLE ClasseMatieres(
            classe INTEGER NOT NULL,
            matiere INTEGER NOT NULL,
            PRIMARY KEY(matiere, classe),
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table noteexamen
        cursor.execute("""CREATE TABLE NoteExamens(
            matiere INTEGER NOT NULL,
            etudiant INTEGER NOT NULL,
            note_examen FLOAT NOT NULL,
            CHECK(note_examen>=0 AND note_examen<=20),
            PRIMARY KEY(matiere, etudiant),
            update_examen BOOLEAN DEFAULT FALSE,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer la table utilisateur
        cursor.execute("""CREATE TABLE Utilisateurs(
            id_code SERIAL NOT NULL PRIMARY KEY,
            code VARCHAR(6) NOT NULL UNIQUE,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        
        ## creer les relations
        cursor.execute("""ALTER TABLE Etudiants 
            ADD FOREIGN KEY(classe) REFERENCES Classes(id_classe),
            ADD FOREIGN KEY(user_at) REFERENCES Utilisateurs(id_code);"""
        )
        
        cursor.execute("""-ALTER TABLE NoteDevoirs
            ADD FOREIGN KEY(matiere) REFERENCES Matieres(id_matiere),
            ADD FOREIGN KEY(etudiant) REFERENCES Etudiants(id_etudiant);"""
        )
        
        cursor.execute("""ALTER TABLE NoteExamens
            ADD FOREIGN KEY(matiere) REFERENCES Matieres(id_matiere),
            ADD FOREIGN KEY(etudiant) REFERENCES Etudiants(id_etudiant);"""
        )

        cursor.execute("""ALTER TABLE ClasseMatieres
            ADD FOREIGN KEY(matiere) REFERENCES Matieres(id_matiere),
            ADD FOREIGN KEY(classe) REFERENCES Classes(id_classe);"""
        )

        ## valider et fermer la db
        conn.commit()
        cursor.close()
        conn.close()
    except:
        conn.rollback()
        conn.close()