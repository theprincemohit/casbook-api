from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PassbookBase(BaseModel):
    business_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class PassbookCreate(PassbookBase):
    pass


class PassbookUpdate(BaseModel):
    business_id: int
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
   


class Passbook(PassbookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
