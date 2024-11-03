from sqlalchemy.orm import Session
from app.models import User, Receipt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_data):
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_receipt_record(db: Session, current_user: User, receipt_data):
    total = sum(item["price"] * item["quantity"] for item in receipt_data.products)
    rest = receipt_data.payment["amount"] - total
    new_receipt = Receipt(owner_id=current_user.id, total=total)
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return {
        "id": new_receipt.id,
        "products": receipt_data.products,
        "payment": receipt_data.payment,
        "total": total,
        "rest": rest,
        "created_at": new_receipt.created_at
    }