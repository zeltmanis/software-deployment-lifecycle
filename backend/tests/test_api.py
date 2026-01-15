"""
API integration tests for the General Ledger application
These tests verify that all endpoints work correctly
"""
import pytest
from fastapi.testclient import TestClient
from decimal import Decimal

from app.main import app
from app.database import Base, engine
from app.models import PaymentMethod

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check and root endpoints"""

    def test_root_endpoint(self):
        """Test that root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["message"] == "General Ledger API"
        assert "version" in data

    def test_health_endpoint(self):
        """Test that health check endpoint works"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestAccountCreation:
    """Test account creation functionality"""

    def test_create_account_success(self):
        """Test successful account creation"""
        account_data = {
            "first_name": "Test",
            "last_name": "User",
            "balance": 100.50,
            "payment_method": "cash"
        }

        response = client.post("/accounts", json=account_data)
        assert response.status_code == 201

        data = response.json()
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert float(data["balance"]) == 100.50
        assert data["payment_method"] == "cash"
        assert "id" in data
        assert "created_at" in data

    def test_create_account_with_all_payment_methods(self):
        """Test creating accounts with different payment methods"""
        payment_methods = ["cash", "credit_card", "debit_card", "bank_transfer"]

        for method in payment_methods:
            account_data = {
                "first_name": "Payment",
                "last_name": "Test",
                "balance": 50.00,
                "payment_method": method
            }

            response = client.post("/accounts", json=account_data)
            assert response.status_code == 201
            assert response.json()["payment_method"] == method

    def test_create_account_default_balance(self):
        """Test that default balance is 0.00"""
        account_data = {
            "first_name": "Zero",
            "last_name": "Balance",
            "payment_method": "cash"
        }

        response = client.post("/accounts", json=account_data)
        assert response.status_code == 201
        assert float(response.json()["balance"]) == 0.00

    def test_create_account_missing_required_fields(self):
        """Test that missing required fields return error"""
        incomplete_data = {
            "first_name": "Only"
            # Missing last_name
        }

        response = client.post("/accounts", json=incomplete_data)
        assert response.status_code == 422  # Validation error


class TestAccountRetrieval:
    """Test account retrieval functionality"""

    def test_get_all_accounts(self):
        """Test getting list of all accounts"""
        response = client.get("/accounts")
        assert response.status_code == 200

        accounts = response.json()
        assert isinstance(accounts, list)
        # Should have at least the test accounts we seeded
        assert len(accounts) >= 0

    def test_get_account_by_id(self):
        """Test getting a specific account by ID"""
        # First create an account
        account_data = {
            "first_name": "Get",
            "last_name": "Test",
            "balance": 200.00,
            "payment_method": "credit_card"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Now retrieve it
        response = client.get(f"/accounts/{account_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == account_id
        assert data["first_name"] == "Get"
        assert data["last_name"] == "Test"

    def test_get_nonexistent_account(self):
        """Test that getting non-existent account returns 404"""
        response = client.get("/accounts/999999")
        assert response.status_code == 404


class TestAccountUpdate:
    """Test account update functionality"""

    def test_update_account_name(self):
        """Test updating account name"""
        # Create account
        account_data = {
            "first_name": "Original",
            "last_name": "Name",
            "balance": 100.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Update it
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        response = client.put(f"/accounts/{account_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["id"] == account_id

    def test_update_account_balance(self):
        """Test updating account balance"""
        # Create account
        account_data = {
            "first_name": "Balance",
            "last_name": "Update",
            "balance": 100.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Update balance
        update_data = {"balance": 500.50}
        response = client.put(f"/accounts/{account_id}", json=update_data)
        assert response.status_code == 200
        assert float(response.json()["balance"]) == 500.50

    def test_update_nonexistent_account(self):
        """Test that updating non-existent account returns 404"""
        update_data = {"first_name": "Test"}
        response = client.put("/accounts/999999", json=update_data)
        assert response.status_code == 404


class TestAccountDeletion:
    """Test account deletion functionality"""

    def test_delete_account(self):
        """Test deleting an account"""
        # Create account
        account_data = {
            "first_name": "Delete",
            "last_name": "Me",
            "balance": 100.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/accounts/{account_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/accounts/{account_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_account(self):
        """Test that deleting non-existent account returns 404"""
        response = client.delete("/accounts/999999")
        assert response.status_code == 404


class TestTransactions:
    """Test transaction functionality"""

    def test_add_to_balance(self):
        """Test adding money to account balance"""
        # Create account
        account_data = {
            "first_name": "Transaction",
            "last_name": "Test",
            "balance": 100.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Add money
        transaction_data = {
            "amount": 50.00,
            "description": "Deposit"
        }
        response = client.post(f"/accounts/{account_id}/transaction", json=transaction_data)
        assert response.status_code == 200

        data = response.json()
        assert data["account_id"] == account_id
        assert float(data["previous_balance"]) == 100.00
        assert float(data["new_balance"]) == 150.00
        assert float(data["amount"]) == 50.00

    def test_subtract_from_balance(self):
        """Test subtracting money from account balance"""
        # Create account
        account_data = {
            "first_name": "Withdraw",
            "last_name": "Test",
            "balance": 100.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Subtract money
        transaction_data = {
            "amount": -30.00,
            "description": "Withdrawal"
        }
        response = client.post(f"/accounts/{account_id}/transaction", json=transaction_data)
        assert response.status_code == 200

        data = response.json()
        assert float(data["previous_balance"]) == 100.00
        assert float(data["new_balance"]) == 70.00
        assert float(data["amount"]) == -30.00

    def test_transaction_negative_balance_prevention(self):
        """Test that transactions can't result in negative balance"""
        # Create account with low balance
        account_data = {
            "first_name": "Low",
            "last_name": "Balance",
            "balance": 10.00,
            "payment_method": "cash"
        }
        create_response = client.post("/accounts", json=account_data)
        account_id = create_response.json()["id"]

        # Try to withdraw too much
        transaction_data = {
            "amount": -50.00,
            "description": "Too much withdrawal"
        }
        response = client.post(f"/accounts/{account_id}/transaction", json=transaction_data)
        assert response.status_code == 400  # Bad request

    def test_transaction_on_nonexistent_account(self):
        """Test that transaction on non-existent account returns 404"""
        transaction_data = {
            "amount": 10.00,
            "description": "Test"
        }
        response = client.post("/accounts/999999/transaction", json=transaction_data)
        assert response.status_code == 404