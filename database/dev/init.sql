-- Development database initialization script
-- This script creates the database schema for the dev environment

CREATE DATABASE IF NOT EXISTS ledger_dev;
USE ledger_dev;

-- The tables will be created automatically by SQLAlchemy
-- This file can be used for any custom dev setup if needed

-- Grant permissions to dev user
GRANT ALL PRIVILEGES ON ledger_dev.* TO 'dev_user'@'%';
FLUSH PRIVILEGES;