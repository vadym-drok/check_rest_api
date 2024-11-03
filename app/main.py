from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import UserCreate, UserResponse, ReceiptCreate, ReceiptResponse
from app.crud import get_user_by_username, create_user, create_receipt_record


app = FastAPI(docs_url='/')


# User registration endpoint
@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = create_user(db, user)
    return new_user


# @app.post('/login', response_model=Token)
# def login():
#     pass


# Create receipt endpoint
@app.post("/receipts", response_model=ReceiptResponse)
def create_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_receipt = create_receipt_record(db, current_user, receipt)
    return new_receipt


# Initialize database
def init_db():
    from app.database import engine, Base
    Base.metadata.create_all(bind=engine)


init_db()
