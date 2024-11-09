from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Receipt
from app.schemas import ReceiptCreate, ReceiptResponse
from app.crud import create_receipt_record
from app.utils import verify_access_token


router = APIRouter(
    prefix='/receipts',
    tags=['Receipts'],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReceiptResponse)
def create_receipt(
        receipt_data: ReceiptCreate, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)
):
    receipt = create_receipt_record(db, current_user, receipt_data)
    response = ReceiptResponse(
        id=receipt.id,
        products=receipt_data.products,
        payment=receipt_data.payment,
        total=receipt.total,
        rest=receipt.rest,
        created_at=receipt.created_at
    )

    return response


@router.get('/{id}', response_model=ReceiptResponse)
def get_receipt(id: str, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)):
    receipt =  db.query(Receipt).filter(Receipt.id == id, Receipt.owner_id == current_user.id).first()

    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    response = ReceiptResponse(
        id=receipt.id,
        products=receipt.raw_data['products'],
        payment=receipt.raw_data['payment'],
        total=receipt.total,
        rest=receipt.rest,
        created_at=receipt.created_at
    )

    return response


@router.get('/{id}')
def get_receipt_by_link(id: str, row_length: int = 20, db: Session = Depends(get_db)):
    # 19 < row_length < 120
    return  # str


@router.get('/', response_model=List[ReceiptResponse])
def get_receipts(
        db: Session = Depends(get_db),
        current_user: User = Depends(verify_access_token),
        skip: int = 0, search: Optional[str] = ''
):
    pass
