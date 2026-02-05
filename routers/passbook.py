from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from schema.business import Business, BusinessCreate, BusinessUpdate
from config import get_db
import database

router = APIRouter(prefix="/passbook", tags=["passbook"])


@router.post("/", response_model=Business, status_code=201)
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    """Create a new passbook"""
    new_business = database.create_business(db, business.model_dump())
    return new_business


@router.get("/", response_model=List[Business])
def read_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    industry: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all passbooks with optional filtering and pagination"""
    return database.get_all_businesses(db, skip=skip, limit=limit, industry=industry)


@router.get("/{passbook_id}", response_model=Business)
def read_business(passbook_id: int, db: Session = Depends(get_db)):
    """Get a specific passbook by ID"""
    business = database.get_business(db, passbook_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return business


@router.put("/{passbook_id}", response_model=Business)
def update_business(
    passbook_id: int, updated_business: BusinessCreate, db: Session = Depends(get_db)
):
    """Update a passbook"""
    business = database.update_business(db, passbook_id, updated_business.model_dump())
    if business is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return business


@router.patch("/{passbook_id}", response_model=Business)
def partial_update_business(
    passbook_id: int,
    passbook_update: BusinessUpdate,
    db: Session = Depends(get_db),
):
    """Partially update a passbook"""
    business = database.partial_update_business(
        db, passbook_id, passbook_update.model_dump(exclude_unset=True)
    )
    if business is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return business


@router.delete("/{passbook_id}", status_code=204)
def delete_business(passbook_id: int, db: Session = Depends(get_db)):
    """Delete a passbook"""
    success = database.delete_business(db, passbook_id)
    if not success:
        raise HTTPException(status_code=404, detail="Passbook not found")

@router.get("/stats/overview")
def get_statistics(db: Session = Depends(get_db)):
    """Get statistics about all passbooks"""
    return database.get_statistics(db)
