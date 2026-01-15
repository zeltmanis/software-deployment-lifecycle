"""
Database models for the General Ledger application
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .database import Base


class PaymentMethod(str, enum.Enum):
    """Enum for payment methods"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"


class Account(Base):
    """
    Account model representing a customer account in the ledger
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00, nullable=False)
    payment_method = Column(
        Enum(PaymentMethod),
        default=PaymentMethod.CASH,
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Account(id={self.id}, name={self.first_name} {self.last_name}, balance={self.balance})>"