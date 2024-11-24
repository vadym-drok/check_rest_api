import json
from typing import Dict

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime
from app.database import Base
from app.services import DecimalEncoder
import enum


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    receipts = relationship("Receipt", back_populates="owner")


class PaymentType(enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Receipt(Base):
    """
    TODO:
    Analyze the actual usage of the table – it might be worthwhile to reassess which data should be stored in fields and
    which should be calculated dynamically.
    """
    __tablename__ = 'receipts'
    id = Column(String(12), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    _raw_data = Column(JSON)
    total = Column(DECIMAL(18, 6), nullable=False)
    amount = Column(DECIMAL(18, 6), nullable=False)
    rest = Column(DECIMAL(18, 6), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="receipts")
    payment_type = Column(String(12), nullable=False)

    @property
    def raw_data(self):
        return json.loads(self._raw_data)

    @raw_data.setter
    def raw_data(self, value):
        self._raw_data = json.dumps(value, cls=DecimalEncoder)
