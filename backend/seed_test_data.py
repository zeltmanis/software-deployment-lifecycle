"""
Seed test data into the database
Run this after the database and tables are created
"""
from decimal import Decimal
from app.database import SessionLocal
from app.models import Account, PaymentMethod


def seed_data():
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Account).count()
        if existing_count > 0:
            print(f"ℹ️  Database already has {existing_count} accounts. Skipping seed.")
            return

        # Seed test accounts
        test_accounts = [
            Account(first_name="John", last_name="Doe", balance=Decimal("1000.00"),
                    payment_method=PaymentMethod.CREDIT_CARD),
            Account(first_name="Jane", last_name="Smith", balance=Decimal("2500.50"),
                    payment_method=PaymentMethod.DEBIT_CARD),
            Account(first_name="Alice", last_name="Johnson", balance=Decimal("500.00"),
                    payment_method=PaymentMethod.BANK_TRANSFER),
            Account(first_name="Bob", last_name="Williams", balance=Decimal("3000.00"),
                    payment_method=PaymentMethod.CASH),
            Account(first_name="Charlie", last_name="Brown", balance=Decimal("150.75"),
                    payment_method=PaymentMethod.CREDIT_CARD),
            Account(first_name="Diana", last_name="Martinez", balance=Decimal("4200.00"),
                    payment_method=PaymentMethod.BANK_TRANSFER),
            Account(first_name="Edward", last_name="Davis", balance=Decimal("750.25"),
                    payment_method=PaymentMethod.DEBIT_CARD),
            Account(first_name="Fiona", last_name="Garcia", balance=Decimal("1800.00"),
                    payment_method=PaymentMethod.CASH),
            Account(first_name="George", last_name="Rodriguez", balance=Decimal("5000.00"),
                    payment_method=PaymentMethod.CREDIT_CARD),
            Account(first_name="Hannah", last_name="Wilson", balance=Decimal("320.50"),
                    payment_method=PaymentMethod.BANK_TRANSFER),
        ]

        db.add_all(test_accounts)
        db.commit()

        print(f"✅ Successfully seeded {len(test_accounts)} test accounts!")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()