-- Test database initialization and seeding script
-- This script creates clean test data that gets loaded every time test environment starts

CREATE DATABASE IF NOT EXISTS ledger_test;
USE ledger_test;

-- The tables will be created automatically by SQLAlchemy

-- Seed test data - always the same accounts for consistent testing
INSERT INTO accounts (first_name, last_name, balance, payment_method, created_at) VALUES
('John', 'Doe', 1000.00, 'credit_card', NOW()),
('Jane', 'Smith', 2500.50, 'debit_card', NOW()),
('Alice', 'Johnson', 500.00, 'bank_transfer', NOW()),
('Bob', 'Williams', 3000.00, 'cash', NOW()),
('Charlie', 'Brown', 150.75, 'credit_card', NOW()),
('Diana', 'Martinez', 4200.00, 'bank_transfer', NOW()),
('Edward', 'Davis', 750.25, 'debit_card', NOW()),
('Fiona', 'Garcia', 1800.00, 'cash', NOW()),
('George', 'Rodriguez', 5000.00, 'credit_card', NOW()),
('Hannah', 'Wilson', 320.50, 'bank_transfer', NOW());

-- Grant permissions to test user
GRANT ALL PRIVILEGES ON ledger_test.* TO 'test_user'@'%';
FLUSH PRIVILEGES;