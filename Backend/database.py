import psycopg2

def connexion():
    try:
        return psycopg2.connect(
            database = 'gestionecole',
            user = 'postgres',
            password = '',
            host = 'localhost',
            port = 5432
        )
    except psycopg2.errors as e:
        print(f'ERREUR: {e}')
