from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=200)
    email: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    photo: Optional[str] = Field(None, max_length=200)

class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    photo: Optional[str] = Field(None, max_length=200)
   
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



class User(UserBase):

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
