-- AIRO Finance Lab — MVP Database Schema (PostgreSQL / Supabase)
-- Version: 1.0.0
-- Tables: accounts, categories, transactions, budgets, audit_logs
-- Status: LOCKED_MVP_SCHEMA

-- 1. Accounts
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL, -- 'BANK', 'CASH', 'E_WALLET', 'CREDIT_CARD'
    balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Categories
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    category_id TEXT REFERENCES categories(id) ON DELETE RESTRICT,
    amount NUMERIC(15, 2) NOT NULL CHECK (amount > 0),
    direction TEXT NOT NULL, -- 'EXPENSE', 'INCOME', 'TRANSFER'
    note TEXT,
    source TEXT NOT NULL DEFAULT 'MANUAL', -- 'TELEGRAM', 'MANUAL', 'DASHBOARD'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Budgets
CREATE TABLE IF NOT EXISTS budgets (
    id TEXT PRIMARY KEY,
    category_id TEXT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    month TEXT NOT NULL, -- 'YYYY-MM'
    limit_amount NUMERIC(15, 2) NOT NULL CHECK (limit_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (category_id, month)
);

-- 5. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    entity TEXT NOT NULL, -- 'transactions', 'accounts', 'categories', 'budgets'
    entity_id TEXT NOT NULL,
    action TEXT NOT NULL, -- 'CREATE', 'UPDATE', 'VOID', 'DELETE'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
