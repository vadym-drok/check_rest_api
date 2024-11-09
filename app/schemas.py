from decimal import Decimal

from pydantic import BaseModel, validator
from typing import List, Union, Dict
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Payment(BaseModel):
    type: str
    amount: Decimal


class Product(BaseModel):
    name: str
    price: Decimal
    quantity: int
    total: Decimal = None

    @validator('total', pre=True, always=True)
    def calculate_total(cls, value, values):
        return round(values['price'] * values['quantity'], 6)


class ReceiptCreate(BaseModel):
    products: List[Product]
    payment: Payment
    add_info: Union[Dict, None] = None


class ReceiptResponse(BaseModel):
    id: str
    products: List[Product]
    payment: Payment
    total: Decimal
    rest: Decimal
    created_at: datetime
