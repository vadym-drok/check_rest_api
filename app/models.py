import json
from decimal import Decimal

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    receipts = relationship("Receipt", back_populates="owner")


class Receipt(Base):
    __tablename__ = 'receipts'
    id = Column(String(12), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    raw_data = Column(JSON)
    owner = relationship("User", back_populates="receipts")

    @property
    def total(self):
        raw_data = json.loads(self.raw_data)
        total = Decimal(sum(item['price'] * item['quantity'] for item in raw_data['products']))
        return round(total, 6)

    @property
    def rest(self):
        raw_data = json.loads(self.raw_data)
        return round(Decimal(raw_data['payment']['amount']) - self.total, 6)


class PaymentType():
    __tablename__ = 'payment_types'
    code = Column(String, primary_key=True, index=True)
    name = Column(String)
