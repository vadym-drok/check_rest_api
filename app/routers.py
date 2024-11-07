from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import User, Receipt
from app.schemas import UserCreate, UserResponse, Token, ReceiptCreate, ReceiptResponse
from app.crud import create_user, create_access_token, create_receipt_record
from app.utils import get_user_by_username, authenticate_user, verify_access_token

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = create_user(db, user)
    return new_user


@router.post('/login', response_model=Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token_data = {
        "username": user.username,
    }
    access_token = create_access_token(token_data)
    return access_token


@router.post("/receipts", status_code=status.HTTP_201_CREATED, response_model=ReceiptResponse)
def create_receipt(
        receipt: ReceiptCreate, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)
):
    new_receipt = create_receipt_record(db, current_user, receipt)
    # new_receipt = Receipt(owner_id=current_user.id, total=100)
    # db.add(new_receipt)
    # db.commit()
    # db.refresh(new_receipt)
    # print(ReceiptResponse.from_orm(new_receipt))
    # response = ReceiptResponse.from_orm(new_receipt)
    return new_receipt
