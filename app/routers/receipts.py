from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Receipt
from app.schemas import ReceiptCreate, ReceiptResponse
from app.crud import create_receipt_record
from app.utils import verify_access_token, create_receipt_preview

router = APIRouter(
    prefix='/receipts',
    tags=['Receipts'],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReceiptResponse)
def create_receipt(
        receipt_data: ReceiptCreate, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)
):
    receipt = create_receipt_record(db, current_user, receipt_data)

    return ReceiptResponse.from_orm_with_nested(receipt)


@router.get('/{id}', response_model=ReceiptResponse)
def get_receipt(id: str, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)):
    receipt = db.query(Receipt).filter(Receipt.id == id, Receipt.owner_id == current_user.id).first()

    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    return ReceiptResponse.from_orm_with_nested(receipt)


@router.get('/{id}/preview/', response_class=PlainTextResponse)
def get_receipt_preview(id: str, line_length: int = 20, db: Session = Depends(get_db)):
    receipt = db.query(Receipt).filter(Receipt.id == id).first()

    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    if line_length < 19 or line_length > 120:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="row_length must be from 20 to 120")

    receipt_preview = create_receipt_preview(receipt, line_length)

    return  receipt_preview


@router.get('/', response_model=List[ReceiptResponse])
def get_receipts(
        db: Session = Depends(get_db),
        current_user: User = Depends(verify_access_token),
        skip: int = 0,
        limit: int = 10,

        # date_from: Optional[datetime] = Query(None, description="Filter receipts created after this date"),
        # date_to: Optional[datetime] = Query(None, description="Filter receipts created before this date"),
        # min_total: Optional[float] = Query(None, description="Filter receipts with total greater than this amount"),
        # max_total: Optional[float] = Query(None, description="Filter receipts with total less than this amount"),
        # payment_type: Optional[str] = Query(None, description="Filter receipts by payment type"),
):
    receipts = db.query(Receipt).filter(Receipt.owner_id == current_user.id)\
        .limit(limit)\
        .offset(skip)

    # results = db.query(Post, func.count(Vote.post_id).label('votes'))\
    #     .join(Vote, Vote.post_id == Post.id, isouter=True)\
    #     .group_by(Post.id)\
    #     .filter(Post.title.contains(search))\
    #     .limit(limit)\
    #     .offset(skip)

    if receipts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No receipts were found for this user")

    response = [ReceiptResponse.from_orm_with_nested(receipt) for receipt in receipts]

    return response