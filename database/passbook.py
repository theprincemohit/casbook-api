from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.passbook import PassbookModel


def create_new_passbook(db: Session, passbook_data: dict) -> PassbookModel:
    """Create a new passbook in database"""
    db_passbook = PassbookModel(**passbook_data)
    db.add(db_passbook)
    db.commit()
    db.refresh(db_passbook)
    return db_passbook


def get_all_passbooks(
    db: Session, skip: int = 0, limit: int = 10, industry: Optional[str] = None
) -> List[PassbookModel]:
    """Get all passbooks with optional filtering"""
    query = db.query(PassbookModel)

    if industry:
        query = query.filter(
            func.lower(PassbookModel.industry) == func.lower(industry)
        )

    return query.offset(skip).limit(limit).all()


def get_passbook(db: Session, passbook_id: int) -> Optional[PassbookModel]:
    """Get a specific passbook by ID"""
    return db.query(PassbookModel).filter(PassbookModel.id == passbook_id).first()


def update_passbook(
    db: Session, passbook_id: int, passbook_data: dict
) -> Optional[PassbookModel]:
    """Update a passbook"""
    db_passbook = db.query(PassbookModel).filter(PassbookModel.id == passbook_id).first()
    if db_passbook is None:
        return None

    for key, value in passbook_data.items():
        setattr(db_passbook, key, value)

    db.commit()
    db.refresh(db_passbook)
    return db_passbook


def partial_update_passbook(
    db: Session, passbook_id: int, passbook_data: dict
) -> Optional[PassbookModel]:
    """Partially update a passbook"""
    db_passbook = db.query(PassbookModel).filter(PassbookModel.id == passbook_id).first()
    if db_passbook is None:
        return None

    # Only update provided fields
    allowed_fields = {
        "name",
        "description",
    }

    for key, value in passbook_data.items():
        if key in allowed_fields and value is not None:
            setattr(db_passbook, key, value)

    db.commit()
    db.refresh(db_passbook)
    return db_passbook


def delete_passbook(db: Session, passbook_id: int) -> bool:
    """Delete a passbook"""
    db_passbook = db.query(PassbookModel).filter(PassbookModel.id == passbook_id).first()
    if db_passbook is None:
        return False

    db.delete(db_passbook)
    db.commit()
    return True


def get_statistics(db: Session) -> dict:
    """Get statistics about all passbooks"""
    count = db.query(func.count(PassbookModel.id)).scalar()

    if count == 0:
        return {
            "total_passbooks": 0,
        }

   

    return {
        "total_passbooks": count,
    }
