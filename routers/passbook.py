from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from routers.auth import validate_token
from schema.passbook import Passbook, PassbookCreate, PassbookUpdate
from config import get_db
import database.passbook as database_passbook 

router = APIRouter(prefix="/passbook", tags=["passbook"])


@router.post("/", response_model=Passbook, status_code=201)
def create_passbook(passbook: PassbookCreate, 
                    db: Session = Depends(get_db),
                    current_user = Depends(validate_token)):
    """Create a new passbook"""
    data  = passbook.model_dump()
    data["user_id"] = current_user.id
    new_passbook = database_passbook.create_new_passbook(db, data)
    return new_passbook

@router.get("/{business_id}", response_model=List[Passbook])
def read_passbooks(
    business_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(validate_token)
):
    """Get all passbooks with optional filtering and pagination"""
    return database_passbook.get_all_passbooks(db, skip=skip, limit=limit, business_id=business_id, current_user=current_user)


@router.get("/{business_id}/{passbook_id}", response_model=Passbook)
def read_passbook(business_id: int, passbook_id: int, db: Session = Depends(get_db),
                    current_user = Depends(validate_token),
                    ):
    """Get a specific passbook by ID"""
    passbook = database_passbook.get_passbook(db, passbook_id, 
                                              current_user=current_user, 
                                              business_id=business_id)
    if passbook is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return passbook


@router.patch("/{business_id}/{passbook_id}", response_model=Passbook)
def partial_update_passbook(
    business_id: int,
    passbook_id: int,
    passbook_update: PassbookUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(validate_token)
):
    """Partially update a passbook"""
    passbook = database_passbook.partial_update_passbook(
        db, business_id, current_user, passbook_id, passbook_update.model_dump(exclude_unset=True)
    )
    if passbook is None:
        raise HTTPException(status_code=404, detail="Passbook not found")
    return passbook


@router.delete("/{business_id}/{passbook_id}", status_code=204)
def delete_passbook(business_id: int, passbook_id: int, db: Session = Depends(get_db),
                    current_user = Depends(validate_token)):
    """Delete a passbook"""
    success = database_passbook.delete_passbook(db, passbook_id, current_user=current_user, business_id=business_id)
    if not success:
        raise HTTPException(status_code=404, detail="Passbook not found")

@router.get("/stats/overview")
def get_statistics(db: Session = Depends(get_db)):
    """Get statistics about all passbooks"""
    return database_passbook.get_statistics(db)
