from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import UserModel
from fastapi import HTTPException
import routers.auth as auth


def create_new_user(db: Session, user_data: dict) -> dict:
    """Create a new user in database"""
    existing_user = db.query(UserModel).filter(UserModel.username == user_data["username"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = auth.hash_password(user_data["password"])
    new_user = UserModel(name=user_data["name"], phone=user_data["phone"],photo=user_data["photo"], username=user_data["username"], email=user_data["email"], password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = auth.create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}



def get_all_users(
    db: Session, skip: int = 0, limit: int = 10, passbook_id: Optional[int] = None
) -> List[UserModel]:
    """Get all users with optional filtering"""
    query = db.query(UserModel)

    if passbook_id is not None:
        query = query.filter(UserModel.passbook_id == passbook_id)

    return query.offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> Optional[UserModel]:
    """Get a specific user by ID"""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def update_user(
    db: Session, user_id: int, user_data: dict
) -> Optional[UserModel]:
    """Update a user"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        return None

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def partial_update_user(
    db: Session, user_id: int, user_data: dict
) -> Optional[UserModel]:
    """Partially update a user"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        return None

    # Only update provided fields
    allowed_fields = {
        "description",
    }

    for key, value in user_data.items():
        if key in allowed_fields and value is not None:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        return False

    db.delete(db_user)
    db.commit()
    return True

def login(db: Session, user_data: dict) -> Optional[UserModel]:
    """Login user"""
    db_user = db.query(UserModel).filter(UserModel.username == user_data["username"]).first()
    if not db_user or not auth.verify_password(user_data["password"], db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
