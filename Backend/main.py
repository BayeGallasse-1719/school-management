from fastapi import FastAPI
from routes import import_json, etudiants
from fastapi.middleware.cors import CORSMiddleware

## instancier l'app fastapi
app = FastAPI(
    title='Gestion Ecole',
    description="Application de Gestion d'ecole",
    version='0.0.1'
)

# configuration cors complete
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null",  # Pour les fichiers ouverts directement
        "file://",  # Pour les protocoles file://
        "*"  # En développement uniquement - accepte toutes les origines
    ],
    allow_credentials = True,
    allow_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers = ['*'],
    expose_headers = ['*'],
)


## route principal
@app.get('/api/v1/health')
async def health():
    return {'welcome' : 'Gestion ecole'}

## route chargement json
app.include_router(import_json.router) 

## get all student
app.include_router(etudiants.router)
    
