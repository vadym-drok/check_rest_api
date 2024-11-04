from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class ReceiptCreate(BaseModel):
    products: List[dict]
    payment: dict


class ReceiptResponse(BaseModel):
    id: int
    products: List[dict]
    payment: dict
    total: float
    rest: float
    created_at: datetime
