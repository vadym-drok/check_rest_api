from datetime import timedelta, datetime, timezone
from typing import Union
from sqlalchemy.orm import Session
from app.models import User, Receipt
from app.schemas import Token, ReceiptCreate
from app.utils import get_password_hash
import jwt
from app.config import settings


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return Token(access_token=encoded_jwt, token_type="bearer")


def create_user(db: Session, user_data: dict):
    user_data.password = get_password_hash(user_data.password)
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_receipt_record(db: Session, current_user: User, receipt_data: ReceiptCreate):
#     total = sum(item["price"] * item["quantity"] for item in receipt_data.products)
#     rest = receipt_data.payment["amount"] - total
    new_receipt = Receipt(owner_id=current_user.id, total=100)
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    return new_receipt
#     return {
#         "id": new_receipt.id,
#         "products": receipt_data.products,
#         "payment": receipt_data.payment,
#         "total": total,
#         "rest": rest,
#         "created_at": new_receipt.created_at
#     }
