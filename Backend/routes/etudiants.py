"""
Routes API Étudiants
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date
import math

from requetes import etudiants, classe, utilisateurs, matiere, devoir, examen
from shema import (
    EtudiantResponse,
    Etudiant,
    UpdateEtudiant,
    EtudiantDetailResponse,
    NoteDetail,
    PaginatedResponse,
    NoteDevoirCreate,
    NoteExamenCreate,
)

router = APIRouter(prefix="/api/v1", tags=["Étudiants"])


@router.get("/etudiants", response_model=PaginatedResponse)
async def liste_etudiants(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    classe_filter: Optional[str] = Query(None, alias="classe"),
    source: Optional[str] = Query(None),
    archive: bool = Query(False),
):
    """Liste paginée + recherche + filtres"""
    rows, total = etudiants.afficher_etudiants(
        page=page,
        limit=limit,
        search=search,
        classe=classe_filter,
        source=source,
        archive=archive,
    )

    data = [
        EtudiantResponse(
            numero=r[0],
            nom=r[1],
            prenom=r[2],
            date_naissance=r[3],
            user_at=r[4] or "",
            classe=r[5] or "",
            source=r[6] or "DB",
            archive=r[7] if len(r) > 7 else False,
        )
        for r in rows
    ]

    pages = math.ceil(total / limit) if limit else 1

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        pages=pages,
        data=data,
    )


@router.get("/etudiants/{numero}", response_model=EtudiantDetailResponse)
async def detail_etudiant(numero: str):
    """Détail complet d'un étudiant avec ses notes"""
    etu = etudiants.get_etudiant_by_numero(numero)
    if not etu:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    # etu = (id, numero, nom, prenom, date_naissance, user_at, classe, source, archive)
    nom_classe = classe.get_classe_by_id(etu[6]) or ""
    code_user = utilisateurs.get_user_by_id(etu[5]) or ""
    notes_raw = etudiants.get_notes_detaillees(numero)

    notes = [
        NoteDetail(
            matiere=n["matiere"],
            note_devoirs=n["note_devoirs"],
            note_examen=n["note_examen"],
            moyenne=n["moyenne"],
        )
        for n in notes_raw
    ]

    return EtudiantDetailResponse(
        numero=etu[1],
        nom=etu[2],
        prenom=etu[3],
        date_naissance=etu[4],
        user_at=code_user,
        classe=nom_classe,
        source=etu[7],
        archive=etu[8] if len(etu) > 8 else False,
        notes=notes,
    )


@router.post("/etudiants", status_code=201)
async def creer_etudiant(payload: Etudiant):
    """Création d'un étudiant"""
    if etudiants.get_etudiant_by_numero(payload.numero):
        raise HTTPException(status_code=409, detail="Ce numéro existe déjà")

    # Classe
    cl = classe.get_classe_by_nom(payload.classe)
    if not cl:
        id_classe = classe.ajouter_classe(payload.classe)
    else:
        id_classe = cl[0]

    # Utilisateur
    us = utilisateurs.get_user_by_code(payload.user_at)
    if not us:
        id_user = utilisateurs.ajouter_user(payload.user_at)
    else:
        id_user = us[0]

    id_etu = etudiants.ajouter_etudiant(
        nom=payload.nom,
        prenom=payload.prenom,
        numero=payload.numero,
        date_naissance=payload.date_naissance,
        user_id=id_user,
        classe_id=id_classe,
        source=payload.source or "DB",
    )

    return {"message": "Étudiant créé", "id": id_etu, "numero": payload.numero}


@router.put("/etudiants/{numero}")
async def modifier_etudiant(numero: str, payload: UpdateEtudiant):
    """Mise à jour partielle"""
    if not etudiants.get_etudiant_by_numero(numero):
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    id_user = None
    id_classe = None

    if payload.user_at:
        us = utilisateurs.get_user_by_code(payload.user_at)
        if not us:
            id_user = utilisateurs.ajouter_user(payload.user_at)
        else:
            id_user = us[0]

    if payload.classe:
        cl = classe.get_classe_by_nom(payload.classe)
        if not cl:
            id_classe = classe.ajouter_classe(payload.classe)
        else:
            id_classe = cl[0]

    etudiants.update_etudiant(
        numero=numero,
        nom=payload.nom,
        prenom=payload.prenom,
        date_naissance=payload.date_naissance,
        user_id=id_user,
        classe_id=id_classe,
        archive=payload.archive,
    )

    return {"message": "Étudiant mis à jour", "numero": numero}


@router.patch("/etudiants/{numero}/archiver")
async def archiver(numero: str, archive: bool = True):
    """Archiver / désarchiver un étudiant"""
    if not etudiants.get_etudiant_by_numero(numero):
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    etudiants.archiver_etudiant(numero, archive)
    action = "archivé" if archive else "désarchivé"
    return {"message": f"Étudiant {action}", "numero": numero}


@router.post("/notes/devoir")
async def ajouter_note_devoir(payload: NoteDevoirCreate):
    """Ajouter une note de devoir"""
    etu = etudiants.get_etudiant_by_numero(payload.numero_etudiant)
    if not etu:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    mat = matiere.get_matiere_by_nom(payload.matiere)
    if not mat:
        id_mat = matiere.ajouter_matiere(payload.matiere)
    else:
        id_mat = mat[0]

    devoir.ajouter_devoir(payload.note, id_mat, etu[0])
    return {"message": "Note de devoir ajoutée"}


@router.post("/notes/examen")
async def ajouter_note_examen(payload: NoteExamenCreate):
    """Ajouter / mettre à jour une note d'examen"""
    etu = etudiants.get_etudiant_by_numero(payload.numero_etudiant)
    if not etu:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    mat = matiere.get_matiere_by_nom(payload.matiere)
    if not mat:
        id_mat = matiere.ajouter_matiere(payload.matiere)
    else:
        id_mat = mat[0]

    examen.ajouter_examen(payload.note, id_mat, etu[0])
    return {"message": "Note d'examen enregistrée"}
