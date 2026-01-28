"""
Main FastAPI application entry point
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

from . import models, schemas, crud
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="General Ledger API",
    description="Account balance tracking system for Software Deployment Lifecycle project",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "General Ledger API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# DEMO FEATURE: Uncomment to enable demo endpoint

@app.get("/demo")
async def demo_endpoint():
    '''Demo endpoint to showcase deployment lifecycle'''
    from datetime import datetime
    return {
        "message": "🎉 Demo feature successfully deployed!",
        "timestamp": datetime.now().isoformat(),
        "environment": "production-ready",
        "status": "active"
    }



# Account endpoints

@app.get("/accounts", response_model=List[schemas.AccountResponse])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all accounts with pagination"""
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts


@app.post("/accounts", response_model=schemas.AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    """Create a new account"""
    return crud.create_account(db=db, account=account)


@app.get("/accounts/{account_id}", response_model=schemas.AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get a specific account by ID"""
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.put("/accounts/{account_id}", response_model=schemas.AccountResponse)
def update_account(
    account_id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing account"""
    db_account = crud.update_account(db, account_id=account_id, account_update=account_update)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """Delete an account"""
    success = crud.delete_account(db, account_id=account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return None


@app.post("/accounts/{account_id}/transaction", response_model=schemas.TransactionResponse)
def create_transaction(
    account_id: int,
    transaction: schemas.TransactionRequest,
    db: Session = Depends(get_db)
):
    """Process a transaction (add or subtract from balance)"""
    try:
        result = crud.process_transaction(db, account_id=account_id, amount=transaction.amount)
        if result is None:
            raise HTTPException(status_code=404, detail="Account not found")

        previous_balance, new_balance = result
        return schemas.TransactionResponse(
            account_id=account_id,
            previous_balance=previous_balance,
            new_balance=new_balance,
            amount=transaction.amount,
            description=transaction.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))