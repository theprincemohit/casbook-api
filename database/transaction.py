from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.transaction import TransactionModel


def create_new_transaction(db: Session, transaction_data: dict) -> TransactionModel:
    """Create a new transaction in database"""
    db_transaction = TransactionModel(**transaction_data)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_all_transactions(
    db: Session, skip: int = 0, limit: int = 10, passbook_id: Optional[int] = None
) -> List[TransactionModel]:
    """Get all transactions with optional filtering"""
    query = db.query(TransactionModel)

    if passbook_id is not None:
        query = query.filter(TransactionModel.passbook_id == passbook_id)

    return query.offset(skip).limit(limit).all()


def get_transaction(db: Session, transaction_id: int) -> Optional[TransactionModel]:
    """Get a specific transaction by ID"""
    return db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()


def update_transaction(
    db: Session, transaction_id: int, transaction_data: dict
) -> Optional[TransactionModel]:
    """Update a transaction"""
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if db_transaction is None:
        return None

    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def partial_update_transaction(
    db: Session, transaction_id: int, transaction_data: dict
) -> Optional[TransactionModel]:
    """Partially update a transaction"""
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if db_transaction is None:
        return None

    # Only update provided fields
    allowed_fields = {
        "description",
    }

    for key, value in transaction_data.items():
        if key in allowed_fields and value is not None:
            setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int) -> bool:
    """Delete a transaction"""
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if db_transaction is None:
        return False

    db.delete(db_transaction)
    db.commit()
    return True


def get_statistics(db: Session) -> dict:
    """Get statistics about all transactions"""
    count = db.query(func.count(TransactionModel.id)).scalar()

    if count == 0:
        return {
            "total_transactions": 0,
        }

   

    return {
        "total_transactions": count,
    }
