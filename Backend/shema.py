"""
Schémas Pydantic - Validation des données entrantes/sortantes
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime


# =============================================================================
# Étudiants
# =============================================================================

class EtudiantBase(BaseModel):
    numero: str = Field(..., min_length=7, max_length=7, pattern=r"^[A-Z0-9]{7}$")
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    date_naissance: date
    user_at: str = Field(..., min_length=6, max_length=6, pattern=r"^[A-Z]{3}[0-9]{3}$")
    classe: str = Field(..., min_length=2, max_length=100)


class Etudiant(EtudiantBase):
    """Modèle pour création / modification complète"""
    source: Optional[str] = Field(default="DB", max_length=10)
    archive: Optional[bool] = False


class CreateEtudiant(EtudiantBase):
    source: Optional[str] = "DB"


class UpdateEtudiant(BaseModel):
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    prenom: Optional[str] = Field(None, min_length=2, max_length=100)
    date_naissance: Optional[date] = None
    user_at: Optional[str] = Field(None, min_length=6, max_length=6, pattern=r"^[A-Z]{3}[0-9]{3}$")
    classe: Optional[str] = Field(None, min_length=2, max_length=100)
    archive: Optional[bool] = None


class EtudiantResponse(BaseModel):
    numero: str
    nom: str
    prenom: str
    date_naissance: date
    user_at: str
    classe: str
    source: str
    archive: Optional[bool] = False


class NoteDetail(BaseModel):
    matiere: str
    note_devoirs: List[float] = []
    note_examen: Optional[float] = None
    moyenne: Optional[float] = None


class EtudiantDetailResponse(BaseModel):
    numero: str
    nom: str
    prenom: str
    date_naissance: date
    user_at: str
    classe: str
    source: Optional[str] = None
    archive: Optional[bool] = False
    notes: List[NoteDetail] = []


# =============================================================================
# Notes
# =============================================================================

class NoteDevoirCreate(BaseModel):
    note: float = Field(..., ge=0, le=20)
    matiere: str
    numero_etudiant: str


class NoteExamenCreate(BaseModel):
    note: float = Field(..., ge=0, le=20)
    matiere: str
    numero_etudiant: str


class UpdateNote(BaseModel):
    note: float = Field(..., ge=0, le=20)


# =============================================================================
# Classes / Matières / Utilisateurs
# =============================================================================

class Classe(BaseModel):
    nom_classe: str = Field(..., min_length=2, max_length=100)


class Matiere(BaseModel):
    nom_matiere: str = Field(..., min_length=2, max_length=100)


class Utilisateur(BaseModel):
    code: str = Field(..., min_length=6, max_length=6, pattern=r"^[A-Z]{3}[0-9]{3}$")


# =============================================================================
# Pagination & Recherche
# =============================================================================

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    search: Optional[str] = None
    classe: Optional[str] = None
    source: Optional[str] = None
    archive: Optional[bool] = False


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    data: List[EtudiantResponse]


# =============================================================================
# Dashboard
# =============================================================================

class StatsDashboard(BaseModel):
    total_etudiants: int
    total_classes: int
    total_matieres: int
    etudiants_par_classe: List[dict]
    etudiants_par_source: List[dict]
    moyenne_generale: Optional[float] = None
    top_etudiants: List[dict] = []
    repartition_notes: List[dict] = []
