from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    passbook_id: int
   # name: str = Field(..., min_length=1, max_length=100)
    txn_type: str = Field(..., max_length=500)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    txn_date: Optional[datetime] = None
    reference_no: Optional[str] = Field(None, max_length=50)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    passbook_id: int
  #  name: Optional[str] = Field(None, min_length=1, max_length=100)
    txn_type: str = Field(..., max_length=500)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    txn_date: Optional[datetime] = None
    reference_no: Optional[str] = Field(None, max_length=50)
   


class Transaction(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
