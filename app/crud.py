import json

from datetime import timedelta, datetime, timezone
from typing import Union
from sqlalchemy.orm import Session
from app.models import User, Receipt
from app.schemas import Token, ReceiptCreate
from app.utils import get_password_hash, DecimalEncoder, generate_random_id
import jwt
from app.config import settings


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
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
    receipt = Receipt(owner_id=current_user.id, raw_data=raw_data, id=generate_random_id())
    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    return receipt
