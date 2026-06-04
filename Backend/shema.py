from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

#----------------------------------------------------------------------------------------------------------------------------
##      Etudiants
#-----------------------------------------------------------------------------------------------------------------------------

class Etudiant(BaseModel):
    numero: str = Field(..., max_length=7, pattern=r'^[A-Z0-9]{7}$')
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    date_naissance: date
    user_at: str
    classe: str
    source: str = Field(default="DB", max_length=10)
    archive: bool = Field(default=False)

class CreateEtudiant(BaseModel):
    numero: str = Field(..., max_length=7, pattern=r'^[A-Z0-9]{7}$')
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    date_naissance: date
    user_at: int
    classe: int
    source: str = Field(default="DB", max_length=10)
    archive: bool = Field(default=False)

class UpdateEtudiant(BaseModel):
    #numero: Optional[str] = Field(None, max_length=7)
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    prenom: Optional[str] = Field(None, min_length=2, max_length=100)
    date_naissance: Optional[date] = None
    user_at: Optional[str] = None
    classe: Optional[str] = None
    archive: Optional[bool] = None
    update_etudiant: Optional[bool] = None

class EtudiantResponse(BaseModel):
    numero: str
    nom: str
    prenom: str
    date_naissance: date
    user_at: str 
    classe: str
    source: str



#----------------------------------------------------------------------------------------------------------------------------
##      Matieres
#-----------------------------------------------------------------------------------------------------------------------------

class Matiere(BaseModel):
    nom_matiere: str = Field(..., min_length=2, max_length=100)

#----------------------------------------------------------------------------------------------------------------------------
##      NoteDevoirs
#-----------------------------------------------------------------------------------------------------------------------------

class NoteDevoir(BaseModel):
    note_devoir: float = Field(..., ge=0, le=20)
    matiere: int
    etudiant: int
    update_note: bool = Field(default=False)


class NoteResponse(BaseModel):
    matiere: str    
    note: float

class UpdateNoteDevoir(BaseModel):
    note_devoir: Optional[float] = Field(None, ge=0, le=20)
    matiere: Optional[int] = None
    etudiant: Optional[int] = None
    update_note: Optional[bool] = None

#----------------------------------------------------------------------------------------------------------------------------
##      Classes
#-----------------------------------------------------------------------------------------------------------------------------

class Classe(BaseModel):
    nom_classe: str = Field(..., min_length=2, max_length=100)

#----------------------------------------------------------------------------------------------------------------------------
##      NoteExamens
#-----------------------------------------------------------------------------------------------------------------------------

class NoteExamen(BaseModel):
    matiere: int
    etudiant: int
    note_examen: float = Field(..., ge=0, le=20)
    update_examen: bool = Field(default=False)

class UpdateNoteExamen(BaseModel):
    note_examen: Optional[float] = Field(None, ge=0, le=20)
    update_examen: Optional[bool] = None

#----------------------------------------------------------------------------------------------------------------------------
##      Utilisateurs
#-----------------------------------------------------------------------------------------------------------------------------

class Utilisateur(BaseModel):
    code: str = Field(..., min_length=2, max_length=6, pattern=r'^[A-Z]{3}[0-9]{3}$')

#----------------------------------------------------------------------------------------------------------------------------
##      Detail etudiant
#-----------------------------------------------------------------------------------------------------------------------------

class EtudiantDetailResponse(BaseModel):
    numero: str
    nom: str
    prenom: str
    date_naissance: date
    user_at: str
    classe: str
    source: Optional[str] = None
    notes: List[NoteResponse] = []