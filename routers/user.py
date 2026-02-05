from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from schema.user import User, UserCreate, UserUpdate, Token, UserLogin, UserBase
from config import get_db
import database.user as database_user

router = APIRouter(prefix="", tags=["user"])


@router.post("/login", response_model=Token)
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    new_user = database_user.login(db, user.model_dump())
    return new_user

@router.post("/register", response_model=Token)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    """Register a new user"""
    new_user = database_user.create_new_user(db, user.model_dump())
    return new_user

@router.get("/", response_model=List[User])
def read_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all users with optional filtering and pagination"""
    return database_user.get_all_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)
):
    """Update a user"""
    user = database_user.update_user(db, user_id, updated_user.model_dump())
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

