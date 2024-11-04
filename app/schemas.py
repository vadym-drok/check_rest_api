from pydantic import BaseModel
from typing import List, Union
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
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


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
