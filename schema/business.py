from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BusinessBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    industry: str
    founded_year: int = Field(..., ge=1800, le=2100)
    revenue: float = Field(default=0.0, ge=0)
    employees: int = Field(default=1, ge=1)
    location: str


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    industry: Optional[str] = None
    founded_year: Optional[int] = Field(None, ge=1800, le=2100)
    revenue: Optional[float] = Field(None, ge=0)
    employees: Optional[int] = Field(None, ge=1)
    location: Optional[str] = None


class Business(BusinessBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
