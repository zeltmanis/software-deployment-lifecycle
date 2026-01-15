-- Test database seeding script
-- This script seeds clean test data that gets loaded every time test environment starts
-- Note: The database and tables are created by SQLAlchemy, this only seeds data

USE ledger_test;

-- Clear existing data
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE accounts;
SET FOREIGN_KEY_CHECKS = 1;

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