from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config import Base
from datetime import datetime


class UserModel(Base):
    """SQLAlchemy User model"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    photo = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "phone": self.phone,
            "photo": self.photo,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
