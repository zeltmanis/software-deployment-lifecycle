"""
CRUD operations for database interactions
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from . import models, schemas


def get_account(db: Session, account_id: int) -> Optional[models.Account]:
    """Get a single account by ID"""
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Account]:
    """Get list of accounts with pagination"""
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate) -> models.Account:
    """Create a new account"""
    db_account = models.Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account(
        db: Session,
        account_id: int,
        account_update: schemas.AccountUpdate
) -> Optional[models.Account]:
    """Update an existing account"""
    db_account = get_account(db, account_id)
    if not db_account:
        return None

    # Update only provided fields
    update_data = account_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)

    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: int) -> bool:
    """Delete an account"""
    db_account = get_account(db, account_id)
    if not db_account:
        return False

    db.delete(db_account)
    db.commit()
    return True


def process_transaction(
        db: Session,
        account_id: int,
        amount: Decimal
) -> Optional[tuple[Decimal, Decimal]]:
    """
    Process a transaction (add or subtract from balance)
    Returns tuple of (previous_balance, new_balance) or None if account not found
    """
    db_account = get_account(db, account_id)
    if not db_account:
        return None

    previous_balance = db_account.balance
    new_balance = previous_balance + amount

    if new_balance < 0:
        raise ValueError("Transaction would result in negative balance")

    db_account.balance = new_balance
    db.commit()
    db.refresh(db_account)

    return (previous_balance, new_balance)