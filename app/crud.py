from datetime import timedelta, datetime, timezone
from typing import Union
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from app.schemas import Token, TokenData
from app.utils import get_password_hash, verify_password
import jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return Token(access_token=encoded_jwt, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_access_token(db, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_user(db: Session, user_data):
    user_data.password = get_password_hash(user_data.password)
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# def create_receipt_record(db: Session, current_user: User, receipt_data):
#     total = sum(item["price"] * item["quantity"] for item in receipt_data.products)
#     rest = receipt_data.payment["amount"] - total
#     new_receipt = Receipt(owner_id=current_user.id, total=total)
#     db.add(new_receipt)
#     db.commit()
#     db.refresh(new_receipt)
#     return {
#         "id": new_receipt.id,
#         "products": receipt_data.products,
#         "payment": receipt_data.payment,
#         "total": total,
#         "rest": rest,
#         "created_at": new_receipt.created_at
#     }
