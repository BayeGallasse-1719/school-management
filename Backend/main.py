"""
Application FastAPI - Gestion École
Point d'entrée principal
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routes import etudiants, import_json, dashboard
from database import test_connection

app = FastAPI(
    title="Gestion École",
    description="API complète de gestion d'école - Data Visualisation & CRUD",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS (développement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(etudiants.router)
app.include_router(import_json.router)
app.include_router(dashboard.router)


@app.get("/api/v1/health")
async def health():
    db_ok = test_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "message": "Gestion École API",
    }


# Servir le frontend en production (optionnel)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/dashboard")
    async def serve_dashboard():
        return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
