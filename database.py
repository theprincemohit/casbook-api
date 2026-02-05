from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.business import BusinessModel


def create_business(db: Session, business_data: dict) -> BusinessModel:
    """Create a new business in database"""
    db_business = BusinessModel(**business_data)
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def get_all_businesses(
    db: Session, skip: int = 0, limit: int = 10, industry: Optional[str] = None
) -> List[BusinessModel]:
    """Get all businesses with optional filtering"""
    query = db.query(BusinessModel)

    if industry:
        query = query.filter(
            func.lower(BusinessModel.industry) == func.lower(industry)
        )

    return query.offset(skip).limit(limit).all()


def get_business(db: Session, business_id: int) -> Optional[BusinessModel]:
    """Get a specific business by ID"""
    return db.query(BusinessModel).filter(BusinessModel.id == business_id).first()


def update_business(
    db: Session, business_id: int, business_data: dict
) -> Optional[BusinessModel]:
    """Update a business"""
    db_business = db.query(BusinessModel).filter(BusinessModel.id == business_id).first()
    if db_business is None:
        return None

    for key, value in business_data.items():
        setattr(db_business, key, value)

    db.commit()
    db.refresh(db_business)
    return db_business


def partial_update_business(
    db: Session, business_id: int, business_data: dict
) -> Optional[BusinessModel]:
    """Partially update a business"""
    db_business = db.query(BusinessModel).filter(BusinessModel.id == business_id).first()
    if db_business is None:
        return None

    # Only update provided fields
    allowed_fields = {
        "name",
        "description",
        "industry",
        "founded_year",
        "revenue",
        "employees",
        "location",
    }

    for key, value in business_data.items():
        if key in allowed_fields and value is not None:
            setattr(db_business, key, value)

    db.commit()
    db.refresh(db_business)
    return db_business


def delete_business(db: Session, business_id: int) -> bool:
    """Delete a business"""
    db_business = db.query(BusinessModel).filter(BusinessModel.id == business_id).first()
    if db_business is None:
        return False

    db.delete(db_business)
    db.commit()
    return True


def get_statistics(db: Session) -> dict:
    """Get statistics about all businesses"""
    count = db.query(func.count(BusinessModel.id)).scalar()

    if count == 0:
        return {
            "total_businesses": 0,
            "total_employees": 0,
            "average_revenue": 0.0,
            "industries": [],
        }

    total_employees = db.query(func.sum(BusinessModel.employees)).scalar() or 0
    average_revenue = (
        db.query(func.avg(BusinessModel.revenue)).scalar() or 0.0
    )
    industries = [
        row[0] for row in db.query(BusinessModel.industry.distinct()).all()
    ]

    return {
        "total_businesses": count,
        "total_employees": total_employees,
        "average_revenue": float(average_revenue),
        "industries": industries,
    }
