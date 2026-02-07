from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from routers.auth import validate_token
from schema.business import Business, BusinessCreate, BusinessUpdate
from config import get_db
import database.business as database_business

router = APIRouter(prefix="/businesses", tags=["businesses"])


@router.post("/", response_model=Business, status_code=201)
def create_business(business: BusinessCreate, db: Session = Depends(get_db), current_user = Depends(validate_token)):
    """Create a new business"""
    new_business = database_business.create_new_business(db, business.model_dump())
    return new_business


@router.get("/", response_model=List[Business])
def read_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    industry: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(validate_token)
):
    """Get all businesses with optional filtering and pagination"""
    return database_business.get_all_businesses(db, skip=skip, limit=limit, industry=industry, current_user=current_user)


@router.get("/{business_id}", response_model=Business)
def read_business(business_id: int, db: Session = Depends(get_db)):
    """Get a specific business by ID"""
    business = database_business.get_business(db, business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.put("/{business_id}", response_model=Business)
def update_business(
    business_id: int, updated_business: BusinessCreate, db: Session = Depends(get_db)
):
    """Update a business"""
    business = database_business.update_business(db, business_id, updated_business.model_dump())
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.patch("/{business_id}", response_model=Business)
def partial_update_business(
    business_id: int,
    business_update: BusinessUpdate,
    db: Session = Depends(get_db),
):
    """Partially update a business"""
    business = database_business.partial_update_business(
        db, business_id, business_update.model_dump(exclude_unset=True)
    )
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.delete("/{business_id}", status_code=204)
def delete_business(business_id: int, db: Session = Depends(get_db)):
    """Delete a business"""
    success = database_business.delete_business(db, business_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business not found")


@router.get("/stats/overview")
def get_statistics(db: Session = Depends(get_db)):
    """Get statistics about all businesses"""
    return database_business.get_statistics(db)
