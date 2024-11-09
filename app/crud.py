import json

from datetime import timedelta, datetime, timezone
from decimal import Decimal
from typing import Union
from sqlalchemy.orm import Session
from app.models import User, Receipt
from app.schemas import Token, ReceiptCreate
from app.utils import get_password_hash, DecimalEncoder
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
    raw_data = json.dumps(receipt_data.dict(), cls=DecimalEncoder)
    receipt = Receipt(owner_id=current_user.id, raw_data=raw_data)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    return receipt
