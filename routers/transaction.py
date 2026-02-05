from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from schema.transaction import Transaction, TransactionCreate, TransactionUpdate
from config import get_db
import database.transaction as database_transaction

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/", response_model=Transaction, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction"""
    data  = transaction.model_dump()
    new_transaction = database_transaction.create_new_transaction(db, data)
    return new_transaction

@router.get("/", response_model=List[Transaction])
def read_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all transactions with optional filtering and pagination"""
    return database_transaction.get_all_transactions(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID"""
    transaction = database_transaction.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int, updated_transaction: TransactionUpdate, db: Session = Depends(get_db)
):
    """Update a transaction"""
    transaction = database_transaction.update_transaction(db, transaction_id, updated_transaction.model_dump())
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=Transaction)
def partial_update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Partially update a transaction"""
    transaction = database_transaction.partial_update_transaction(
        db, transaction_id, transaction_update.model_dump(exclude_unset=True)
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction"""
    success = database_transaction.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")

@router.get("/stats/overview")
def get_statistics(db: Session = Depends(get_db)):
    """Get statistics about all transactions"""
    return database_transaction.get_statistics(db)
