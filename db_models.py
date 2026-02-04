from sqlalchemy import Column, Integer, String, Float, DateTime, func
from config import Base
from datetime import datetime


class BusinessModel(Base):
    """SQLAlchemy Business model"""
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    industry = Column(String(100), nullable=False)
    founded_year = Column(Integer, nullable=False)
    revenue = Column(Float, default=0.0)
    employees = Column(Integer, default=1)
    location = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "industry": self.industry,
            "founded_year": self.founded_year,
            "revenue": self.revenue,
            "employees": self.employees,
            "location": self.location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
