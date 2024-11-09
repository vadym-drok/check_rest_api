from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, DECIMAL
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
    total = Column(DECIMAL(18, 6), nullable=False)
    amount = Column(DECIMAL(18, 6), nullable=False)
    rest = Column(DECIMAL(18, 6), nullable=False)
    owner = relationship("User", back_populates="receipts")


class PaymentType():
    __tablename__ = 'payment_types'
    code = Column(String, primary_key=True, index=True)
    name = Column(String)
