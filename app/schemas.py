from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


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
