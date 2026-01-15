"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional

from .models import PaymentMethod


class AccountBase(BaseModel):
    """Base schema for account with common fields"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    payment_method: PaymentMethod = PaymentMethod.CASH


class AccountCreate(AccountBase):
    """Schema for creating a new account"""
    pass


class AccountUpdate(BaseModel):
    """Schema for updating an account (all fields optional)"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    balance: Optional[Decimal] = Field(None, ge=0)
    payment_method: Optional[PaymentMethod] = None


class AccountResponse(AccountBase):
    """Schema for account response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TransactionRequest(BaseModel):
    """Schema for transaction request"""
    amount: Decimal = Field(..., description="Amount to add (positive) or subtract (negative)")
    description: Optional[str] = Field(None, max_length=255)


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    account_id: int
    previous_balance: Decimal
    new_balance: Decimal
    amount: Decimal
    description: Optional[str] = None