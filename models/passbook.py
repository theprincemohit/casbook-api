from sqlalchemy import Column, Integer, String, Float, DateTime, func
from config import Base
from datetime import datetime


class PassbookModel(Base):
    """SQLAlchemy Passbook model"""
    __tablename__ = "passbook"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer(), nullable=False)
    user_id = Column(Integer(), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
