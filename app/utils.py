import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from starlette import status
from typing_extensions import Annotated

from app.database import get_db
from sqlalchemy.orm import Session
from app.config import settings
from app.models import User, Receipt
from app.schemas import TokenData
import random
import string


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
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


def generate_random_id(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_receipt_preview(receipt: Receipt, line_length: int) -> str:
    header = "ФОП Джонсонюк Борис".center(line_length)  # TODO -> move to User LegalEntity
    separator = "=" * line_length
    product_lines = []
    products = receipt.raw_data['products']

    last_product = products[-1]
    for product in products:
        quantity_price = f"{product['quantity']} x {product['price']:.2f}".ljust(line_length // 2)
        total_price = f"{product['quantity'] * product['price']:.2f}".rjust(line_length // 2)
        product_name = product['name'][:line_length].ljust(line_length)
        product_lines.append(f"{quantity_price}{total_price}\n{product_name}")

        if product != last_product:
            product_lines.append("-" * line_length)

    total_line = f"СУМА{str(receipt.total):>{line_length - len('СУМА')}}"
    payment_line = f"Картка{str(receipt.amount):>{line_length - len('Картка')}}"
    rest_line = f"Решта{str(receipt.rest):>{line_length - len('Решта')}}"
    footer = "Дякуємо за покупку!".center(line_length)
    date_time = receipt.created_at.strftime("%d.%m.%Y %H:%M").center(line_length)

    receipt_str = f"{header}\n{separator}\n"
    receipt_str += "\n".join(product_lines) + "\n"
    receipt_str += f"{separator}\n{total_line}\n{payment_line}\n{rest_line}\n{separator}\n{date_time}\n{footer}"

    return receipt_str
