from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from schema.passbook import Passbook, PassbookCreate, PassbookUpdate
from config import get_db
import database.passbook as database_passbook 

router = APIRouter(prefix="/passbook", tags=["passbook"])


@router.post("/", response_model=Passbook, status_code=201)
def create_passbook(passbook: PassbookCreate, db: Session = Depends(get_db)):
    """Create a new passbook"""
    print("Creating passbook with data:", passbook)
    data  = passbook.model_dump()
    print("Data to be inserted into DB:", data)
    new_passbook = database_passbook.create_new_passbook(db, data)
    return new_passbook

@router.get("/", response_model=List[Passbook])
def read_passbooks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    industry: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all passbooks with optional filtering and pagination"""
    return database_passbook.get_all_passbooks(db, skip=skip, limit=limit, industry=industry)


@router.get("/{passbook_id}", response_model=Passbook)
def read_passbook(passbook_id: int, db: Session = Depends(get_db)):
    """Get a specific passbook by ID"""
    passbook = database_passbook.get_passbook(db, passbook_id)
    if passbook is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return passbook


@router.put("/{passbook_id}", response_model=Passbook)
def update_passbook(
    passbook_id: int, updated_passbook: PassbookCreate, db: Session = Depends(get_db)
):
    """Update a passbook"""
    passbook = database_passbook.update_passbook(db, passbook_id, updated_passbook.model_dump())
    if passbook is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return passbook


@router.patch("/{passbook_id}", response_model=Passbook)
def partial_update_passbook(
    passbook_id: int,
    passbook_update: PassbookUpdate,
    db: Session = Depends(get_db),
):
    """Partially update a passbook"""
    passbook = database_passbook.partial_update_passbook(
        db, passbook_id, passbook_update.model_dump(exclude_unset=True)
    )
    if passbook is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return passbook


@router.delete("/{passbook_id}", status_code=204)
def delete_passbook(passbook_id: int, db: Session = Depends(get_db)):
    """Delete a passbook"""
    success = database_passbook.delete_passbook(db, passbook_id)
    if not success:
        raise HTTPException(status_code=404, detail="Passbook not found")

@router.get("/stats/overview")
def get_statistics(db: Session = Depends(get_db)):
    """Get statistics about all passbooks"""
    return database_passbook.get_statistics(db)
