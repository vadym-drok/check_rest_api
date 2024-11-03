from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    id: int

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
