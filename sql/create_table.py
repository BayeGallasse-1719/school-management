#from Backend.database import connexion
import psycopg2
import os
from dotenv import load_dotenv

# Remonte jusqu'à la racine du projet
BASE_DIR = Path(__file__).resolve().parents[1]

# Charge le .env
load_dotenv(BASE_DIR / ".env")

def connexion():
    try:
        return psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    except Exception as e:
        print(f"ERREUR : {e}")

conn = connexion()
 
if conn:
    try:
        cursor = conn.cursor()

        ## 1. Insertion des Classes
        cursor.execute("""
            INSERT INTO Classes (id_classe, nom_classe) VALUES
            (1, '6ème A'),
            (2, '5ème B'),
            (3, '4ème C'),
            (4, '3ème A'),
            (5, 'Seconde S');
        """)

        ## 2. Insertion des Matières
        cursor.execute("""
            INSERT INTO Matieres (id_matiere, nom_matiere) VALUES
            (1, 'Mathématiques'),
            (2, 'Français'),
            (3, 'Histoire-Géographie'),
            (4, 'Physique-Chimie'),
            (5, 'Anglais');
        """)

        ## 3. Insertion des Utilisateurs (100 codes au format 'USR001' à 'USR100' -> Regex ^[A-Z]{3}[0-9]{3}$)
        cursor.execute("""
            INSERT INTO Utilisateurs (id_code, code) VALUES
            (1, 'USR001'), (2, 'USR002'), (3, 'USR003'), (4, 'USR004'), (5, 'USR005'),
            (6, 'USR006'), (7, 'USR007'), (8, 'USR008'), (9, 'USR009'), (10, 'USR010'),
            (11, 'USR011'), (12, 'USR012'), (13, 'USR013'), (14, 'USR014'), (15, 'USR015'),
            (16, 'USR016'), (17, 'USR017'), (18, 'USR018'), (19, 'USR019'), (20, 'USR020'),
            (21, 'USR021'), (22, 'USR022'), (23, 'USR023'), (24, 'USR024'), (25, 'USR025'),
            (26, 'USR026'), (27, 'USR027'), (28, 'USR028'), (29, 'USR029'), (30, 'USR030'),
            (31, 'USR031'), (32, 'USR032'), (33, 'USR033'), (34, 'USR034'), (35, 'USR035'),
            (36, 'USR036'), (37, 'USR037'), (38, 'USR038'), (39, 'USR039'), (40, 'USR040'),
            (41, 'USR041'), (42, 'USR042'), (43, 'USR043'), (44, 'USR044'), (45, 'USR045'),
            (46, 'USR046'), (47, 'USR047'), (48, 'USR048'), (49, 'USR049'), (50, 'USR050'),
            (51, 'USR051'), (52, 'USR052'), (53, 'USR053'), (54, 'USR054'), (55, 'USR055'),
            (56, 'USR056'), (57, 'USR057'), (58, 'USR058'), (59, 'USR059'), (60, 'USR060'),
            (61, 'USR061'), (62, 'USR062'), (63, 'USR063'), (64, 'USR064'), (65, 'USR065'),
            (66, 'USR066'), (67, 'USR067'), (68, 'USR068'), (69, 'USR069'), (70, 'USR070'),
            (71, 'USR071'), (72, 'USR072'), (73, 'USR073'), (74, 'USR074'), (75, 'USR075'),
            (76, 'USR076'), (77, 'USR077'), (78, 'USR078'), (79, 'USR079'), (80, 'USR080'),
            (81, 'USR081'), (82, 'USR082'), (83, 'USR083'), (84, 'USR084'), (85, 'USR085'),
            (86, 'USR086'), (87, 'USR087'), (88, 'USR088'), (89, 'USR089'), (90, 'USR090'),
            (91, 'USR091'), (92, 'USR092'), (93, 'USR093'), (94, 'USR094'), (95, 'USR095'),
            (96, 'USR096'), (97, 'USR097'), (98, 'USR098'), (99, 'USR099'), (100, 'USR100');
        """)

        ## 4. Insertion des Étudiants (Numéros de 7 caractères exacts 'ETU0001' -> Regex ^[A-Z0-9]{7}$)
        cursor.execute("""
            INSERT INTO Etudiants (id_etudiant, numero, nom, prenom, date_naissance, user_at, classe, source) VALUES
            (1, 'ETU0001', 'Diop', 'Moussa', '2006-03-15', 1, 1, 'DB'),
            (2, 'ETU0002', 'Ndiaye', 'Awa', '2005-07-22', 2, 1, 'DB'),
            (3, 'ETU0003', 'Sow', 'Ousmane', '2006-11-05', 3, 2, 'DB'),
            (4, 'ETU0004', 'Fall', 'Fatou', '2005-01-18', 4, 2, 'DB'),
            (5, 'ETU0005', 'Faye', 'Ibrahima', '2006-08-30', 5, 3, 'DB'),
            (6, 'ETU0006', 'Gaye', 'Aminata', '2005-04-12', 6, 3, 'DB'),
            (7, 'ETU0007', 'Ba', 'Cheikh', '2006-09-25', 7, 4, 'DB'),
            (8, 'ETU0008', 'Cissé', 'Mariama', '2005-12-01', 8, 4, 'DB'),
            (9, 'ETU0009', 'Diallo', 'Modou', '2006-02-14', 9, 5, 'DB'),
            (10, 'ETU0010', 'Mbacké', 'Khadija', '2005-06-08', 10, 5, 'DB'),
            (11, 'ETU0011', 'Diop', 'Fatou', '2006-05-19', 11, 1, 'DB'),
            (12, 'ETU0012', 'Ndiaye', 'Moussa', '2005-10-10', 12, 1, 'DB'),
            (13, 'ETU0013', 'Sow', 'Aminata', '2006-01-04', 13, 2, 'DB'),
            (14, 'ETU0014', 'Fall', 'Cheikh', '2005-08-16', 14, 2, 'DB'),
            (15, 'ETU0015', 'Faye', 'Mariama', '2006-04-21', 15, 3, 'DB'),
            (16, 'ETU0016', 'Gaye', 'Modou', '2005-11-29', 16, 3, 'DB'),
            (17, 'ETU0017', 'Ba', 'Khadija', '2006-07-07', 17, 4, 'DB'),
            (18, 'ETU0018', 'Cissé', 'Awa', '2005-03-03', 18, 4, 'DB'),
            (19, 'ETU0019', 'Diallo', 'Ousmane', '2006-12-12', 19, 5, 'DB'),
            (20, 'ETU0020', 'Mbacké', 'Ibrahima', '2005-09-02', 20, 5, 'DB'),
            (21, 'ETU0021', 'Diop', 'Cheikh', '2006-06-11', 21, 1, 'DB'),
            (22, 'ETU0022', 'Ndiaye', 'Mariama', '2005-02-20', 22, 1, 'DB'),
            (23, 'ETU0023', 'Sow', 'Modou', '2006-10-14', 23, 2, 'DB'),
            (24, 'ETU0024', 'Fall', 'Khadija', '2005-05-27', 24, 2, 'DB'),
            (25, 'ETU0025', 'Faye', 'Awa', '2006-08-09', 25, 3, 'DB'),
            (26, 'ETU0026', 'Gaye', 'Ousmane', '2005-12-31', 26, 3, 'DB'),
            (27, 'ETU0027', 'Ba', 'Fatou', '2006-03-01', 27, 4, 'DB'),
            (28, 'ETU0028', 'Cissé', 'Ibrahima', '2005-07-15', 28, 4, 'DB'),
            (29, 'ETU0029', 'Diallo', 'Aminata', '2006-11-22', 29, 5, 'DB'),
            (30, 'ETU0030', 'Mbacké', 'Moussa', '2005-04-05', 30, 5, 'DB'),
            (31, 'ETU0031', 'Diop', 'Awa', '2006-09-17', 31, 1, 'DB'),
            (32, 'ETU0032', 'Ndiaye', 'Ousmane', '2005-01-23', 32, 1, 'DB'),
            (33, 'ETU0033', 'Sow', 'Fatou', '2006-05-06', 33, 2, 'DB'),
            (34, 'ETU0034', 'Fall', 'Ibrahima', '2005-08-19', 34, 2, 'DB'),
            (35, 'ETU0035', 'Faye', 'Aminata', '2006-02-28', 35, 3, 'DB'),
            (36, 'ETU0036', 'Gaye', 'Cheikh', '2005-10-11', 36, 3, 'DB'),
            (37, 'ETU0037', 'Ba', 'Mariama', '2006-07-24', 37, 4, 'DB'),
            (38, 'ETU0038', 'Cissé', 'Modou', '2005-03-18', 38, 4, 'DB'),
            (39, 'ETU0039', 'Diallo', 'Khadija', '2006-12-05', 39, 5, 'DB'),
            (40, 'ETU0040', 'Mbacké', 'Awa', '2005-06-30', 40, 5, 'DB'),
            (41, 'ETU0041', 'Diop', 'Ousmane', '2006-04-14', 41, 1, 'DB'),
            (42, 'ETU0042', 'Ndiaye', 'Fatou', '2005-09-08', 42, 1, 'DB'),
            (43, 'ETU0043', 'Sow', 'Ibrahima', '2006-01-27', 43, 2, 'DB'),
            (44, 'ETU0044', 'Fall', 'Aminata', '2005-11-03', 44, 2, 'DB'),
            (45, 'ETU0045', 'Faye', 'Cheikh', '2006-08-12', 45, 3, 'DB'),
            (46, 'ETU0046', 'Gaye', 'Mariama', '2005-05-21', 46, 3, 'DB'),
            (47, 'ETU0047', 'Ba', 'Modou', '2006-10-02', 47, 4, 'DB'),
            (48, 'ETU0048', 'Cissé', 'Khadija', '2005-02-14', 48, 4, 'DB'),
            (49, 'ETU0049', 'Diallo', 'Moussa', '2006-06-25', 49, 5, 'DB'),
            (50, 'ETU0050', 'Mbacké', 'Awa', '2005-12-19', 50, 5, 'DB'),
            (51, 'ETU0051', 'Diop', 'Ibrahima', '2006-03-09', 51, 1, 'DB'),
            (52, 'ETU0052', 'Ndiaye', 'Aminata', '2005-07-01', 52, 1, 'DB'),
            (53, 'ETU0053', 'Sow', 'Cheikh', '2006-11-15', 53, 2, 'DB'),
            (54, 'ETU0054', 'Fall', 'Mariama', '2005-04-28', 54, 2, 'DB'),
            (55, 'ETU0055', 'Faye', 'Modou', '2006-09-03', 55, 3, 'DB'),
            (56, 'ETU0056', 'Gaye', 'Khadija', '2005-01-11', 56, 3, 'DB'),
            (57, 'ETU0057', 'Ba', 'Moussa', '2006-05-20', 57, 4, 'DB'),
            (58, 'ETU0058', 'Cissé', 'Awa', '2005-10-06', 58, 4, 'DB'),
            (59, 'ETU0059', 'Diallo', 'Ousmane', '2006-02-02', 59, 5, 'DB'),
            (60, 'ETU0060', 'Mbacké', 'Fatou', '2005-08-24', 60, 5, 'DB'),
            (61, 'ETU0061', 'Diop', 'Aminata', '2006-12-18', 61, 1, 'DB'),
            (62, 'ETU0062', 'Ndiaye', 'Cheikh', '2005-03-12', 62, 1, 'DB'),
            (63, 'ETU0063', 'Sow', 'Mariama', '2006-07-29', 63, 2, 'DB'),
            (64, 'ETU0064', 'Fall', 'Modou', '2005-11-10', 64, 2, 'DB'),
            (65, 'ETU0065', 'Faye', 'Khadija', '2006-04-03', 65, 3, 'DB'),
            (66, 'ETU0066', 'Gaye', 'Moussa', '2005-09-15', 66, 3, 'DB'),
            (67, 'ETU0067', 'Ba', 'Awa', '2006-01-08', 67, 4, 'DB'),
            (68, 'ETU0068', 'Cissé', 'Ousmane', '2005-06-22', 68, 4, 'DB'),
            (69, 'ETU0069', 'Diallo', 'Fatou', '2006-10-31', 69, 5, 'DB'),
            (70, 'ETU0070', 'Mbacké', 'Ibrahima', '2005-02-05', 70, 5, 'DB'),
            (71, 'ETU0071', 'Diop', 'Cheikh', '2006-08-17', 71, 1, 'DB'),
            (72, 'ETU0072', 'Ndiaye', 'Mariama', '2005-12-24', 72, 1, 'DB'),
            (73, 'ETU0073', 'Sow', 'Modou', '2006-05-11', 73, 2, 'DB'),
            (74, 'ETU0074', 'Fall', 'Khadija', '2005-09-28', 74, 2, 'DB'),
            (75, 'ETU0075', 'Faye', 'Moussa', '2006-03-04', 75, 3, 'DB'),
            (76, 'ETU0076', 'Gaye', 'Awa', '2005-07-19', 76, 3, 'DB'),
            (77, 'ETU0077', 'Ba', 'Ousmane', '2006-11-08', 77, 4, 'DB'),
            (78, 'ETU0078', 'Cissé', 'Fatou', '2005-04-16', 78, 4, 'DB'),
            (79, 'ETU0079', 'Diallo', 'Ibrahima', '2006-09-01', 79, 5, 'DB'),
            (80, 'ETU0080', 'Mbacké', 'Aminata', '2005-01-25', 80, 5, 'DB'),
            (81, 'ETU0081', 'Diop', 'Mariama', '2006-06-07', 81, 1, 'DB'),
            (82, 'ETU0082', 'Ndiaye', 'Modou', '2005-10-21', 82, 1, 'DB'),
            (83, 'ETU0083', 'Sow', 'Khadija', '2006-02-13', 83, 2, 'DB'),
            (84, 'ETU0084', 'Fall', 'Moussa', '2005-08-04', 84, 2, 'DB'),
            (85, 'ETU0085', 'Faye', 'Awa', '2006-12-29', 85, 3, 'DB'),
            (86, 'ETU0086', 'Gaye', 'Ousmane', '2005-05-17', 86, 3, 'DB'),
            (87, 'ETU0087', 'Ba', 'Fatou', '2006-09-22', 87, 4, 'DB'),
            (88, 'ETU0088', 'Cissé', 'Ibrahima', '2005-01-09', 88, 4, 'DB'),
            (89, 'ETU0089', 'Diallo', 'Aminata', '2006-07-14', 89, 5, 'DB'),
            (90, 'ETU0090', 'Mbacké', 'Cheikh', '2005-11-27', 90, 5, 'DB'),
            (91, 'ETU0091', 'Diop', 'Modou', '2006-04-08', 91, 1, 'DB'),
            (92, 'ETU0092', 'Ndiaye', 'Khadija', '2005-08-20', 92, 1, 'DB'),
            (93, 'ETU0093', 'Sow', 'Moussa', '2006-01-02', 93, 2, 'DB'),
            (94, 'ETU0094', 'Fall', 'Awa', '2005-06-13', 94, 2, 'DB'),
            (95, 'ETU0095', 'Faye', 'Ousmane', '2006-10-26', 95, 3, 'DB'),
            (96, 'ETU0096', 'Gaye', 'Fatou', '2005-03-07', 96, 3, 'DB'),
            (97, 'ETU0097', 'Ba', 'Ibrahima', '2006-07-19', 97, 4, 'DB'),
            (98, 'ETU0098', 'Cissé', 'Aminata', '2005-12-02', 98, 4, 'DB'),
            (99, 'ETU0099', 'Diallo', 'Cheikh', '2006-05-24', 99, 5, 'DB'),
            (100, 'ETU0100', 'Mbacké', 'Mariama', '2005-09-11', 100, 5, 'DB');
        """)

        ## 5. Insertion des Notes Devoirs (Notes entre 0 et 20)
        cursor.execute("""
            INSERT INTO NoteDevoirs (note_devoir, matiere, etudiant) VALUES
            (12.5, 1, 1), (14.0, 1, 1), (10.0, 2, 1), (13.5, 2, 1),
            (15.0, 1, 2), (16.5, 1, 2), (11.0, 2, 2), (09.0, 2, 2),
            (08.5, 1, 3), (12.0, 1, 3), (14.0, 3, 3), (13.0, 3, 3),
            (17.0, 4, 4), (15.5, 4, 4), (12.0, 5, 4), (14.5, 5, 4),
            (11.0, 1, 5), (13.0, 1, 5), (10.5, 2, 5), (12.0, 2, 5);
        """)

        ## 6. Insertion des Notes Examens (Notes entre 0 et 20)
        cursor.execute("""
            INSERT INTO NoteExamens (matiere, etudiant, note_examen) VALUES
            (1, 1, 13.5), (2, 1, 11.0), (3, 1, 14.0), (4, 1, 12.0), (5, 1, 15.0),
            (1, 2, 16.0), (2, 2, 10.5), (3, 2, 13.0), (4, 2, 11.5), (5, 2, 14.0),
            (1, 3, 09.5), (2, 3, 12.0), (3, 3, 13.5), (4, 3, 10.0), (5, 3, 11.0),
            (1, 4, 14.0), (2, 4, 15.0), (3, 4, 12.5), (4, 4, 16.5), (5, 4, 13.0),
            (1, 5, 12.0), (2, 5, 11.0), (3, 5, 10.5), (4, 5, 13.0), (5, 5, 12.5);
        """)

        ## 7. Mise à jour des séquences SERIAL de la base de données
        cursor.execute("SELECT setval('classes_id_classe_seq', (SELECT MAX(id_classe) FROM classes));")
        cursor.execute("SELECT setval('matieres_id_matiere_seq', (SELECT MAX(id_matiere) FROM matieres));")
        cursor.execute("SELECT setval('utilisateurs_id_code_seq', (SELECT MAX(id_code) FROM utilisateurs));")
        cursor.execute("SELECT setval('etudiants_id_etudiant_seq', (SELECT MAX(id_etudiant) FROM etudiants));")

        ## Validation et fermeture
        conn.commit()
        cursor.close()
        conn.close()
        print("Insertion valide et conforme aux modèles Pydantic réalisée avec succès.")

    except Exception as e:
        print(f"Erreur d'insertion : {e}")
        conn.rollback()
        conn.close()