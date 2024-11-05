from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
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


class Receipt(Base):  # TODO
    __tablename__ = 'receipts'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="receipts")
