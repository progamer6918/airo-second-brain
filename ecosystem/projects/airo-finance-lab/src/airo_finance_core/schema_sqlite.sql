-- AIRO Finance Lab — MVP Database Schema (SQLite for local testing/runtime)
-- Version: 1.0.0
-- Tables: accounts, categories, transactions, budgets, audit_logs

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    account_class TEXT NOT NULL DEFAULT 'LIQUID',
    dashboard_group TEXT NOT NULL DEFAULT 'CASH',
    parent_account_id TEXT DEFAULT NULL,
    aliases TEXT NOT NULL DEFAULT '',
    provider TEXT DEFAULT NULL,
    reserve_target_id TEXT DEFAULT NULL
);
CREATE INDEX IF NOT EXISTS idx_accounts_reserve_target ON accounts(reserve_target_id);

-- 2. Categories
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL DEFAULT 1,
    keywords TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 3. Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    account_id TEXT NOT NULL,
    category_id TEXT,
    subcategory_id TEXT,
    amount REAL NOT NULL CHECK (amount > 0),
    direction TEXT NOT NULL,
    note TEXT,
    source TEXT NOT NULL DEFAULT 'MANUAL',
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    credit_card_id TEXT REFERENCES credit_cards(id),
    is_reserved INTEGER NOT NULL DEFAULT 0,
    transfer_side TEXT,
    voided_at TEXT,
    void_reason TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE RESTRICT
);

-- 4. Budgets
CREATE TABLE IF NOT EXISTS budgets (
    id TEXT PRIMARY KEY,
    category_id TEXT NOT NULL,
    month TEXT NOT NULL,
    limit_amount REAL NOT NULL CHECK (limit_amount >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE (category_id, month)
);

-- 5. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    entity TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    action TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 6. Fixed Obligations
CREATE TABLE IF NOT EXISTS fixed_obligations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    due_day INTEGER NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    category_id TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- 7. Finance Configuration
CREATE TABLE IF NOT EXISTS finance_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Default Sane Configurations (Idempotent)
INSERT OR IGNORE INTO finance_config (key, value, updated_at) VALUES ('safety_floor', '1000000.0', datetime('now'));
INSERT OR IGNORE INTO finance_config (key, value, updated_at) VALUES ('payday_day', '25', datetime('now'));

-- 8. Owner Sessions Table (Package 0: Trusted Device & Session Layer)
CREATE TABLE IF NOT EXISTS owner_sessions (
    id TEXT PRIMARY KEY,
    token_hash TEXT NOT NULL UNIQUE,
    device_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at TEXT NOT NULL,
    last_used_at TEXT NOT NULL DEFAULT (datetime('now')),
    revoked_at TEXT
);

-- 9. Assets Table (Package A: Asset Registry)
CREATE TABLE IF NOT EXISTS assets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    current_value REAL NOT NULL CHECK (current_value >= 0),
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    asset_class TEXT DEFAULT 'OTHER',
    weight_grams REAL DEFAULT 0.0,
    purchase_cost REAL DEFAULT 0.0,
    average_cost_per_gram REAL DEFAULT 0.0,
    current_unit_price REAL DEFAULT 0.0
);

-- 10. Liabilities Table (Package A: Liability Registry)
CREATE TABLE IF NOT EXISTS liabilities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    original_amount REAL NOT NULL CHECK (original_amount >= 0),
    remaining_amount REAL NOT NULL CHECK (remaining_amount >= 0),
    monthly_payment REAL NOT NULL CHECK (monthly_payment >= 0),
    due_day INTEGER NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    lender_name TEXT DEFAULT NULL,
    repayment_type TEXT NOT NULL DEFAULT 'INSTALLMENT',
    maturity_date TEXT DEFAULT NULL,
    interest_rate_annual REAL DEFAULT 0.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ====================================================
-- Phase 3.1 Canonical Alignment Schema Extensions
-- ====================================================

-- 11. Subcategories
CREATE TABLE IF NOT EXISTS subcategories (
    id TEXT PRIMARY KEY,
    category_id TEXT NOT NULL,
    name TEXT NOT NULL,
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE(category_id, name)
);
CREATE INDEX IF NOT EXISTS idx_subcategories_category_id ON subcategories(category_id);

-- 12. Category Aliases
CREATE TABLE IF NOT EXISTS category_aliases (
    id TEXT PRIMARY KEY,
    subcategory_id TEXT,
    category_id TEXT,
    keyword TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 10,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_category_aliases_keyword ON category_aliases(keyword);
CREATE INDEX IF NOT EXISTS idx_category_aliases_subcat ON category_aliases(subcategory_id);

-- 13. Transaction Metadata
CREATE TABLE IF NOT EXISTS transaction_metadata (
    transaction_id TEXT PRIMARY KEY,
    subcategory_id TEXT,
    raw_input TEXT,
    source_type TEXT DEFAULT 'MANUAL',
    confidence_score REAL DEFAULT 1.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL
);

-- 14. Correction Events
CREATE TABLE IF NOT EXISTS correction_events (
    id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL,
    field_name TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_correction_events_tx ON correction_events(transaction_id);

-- 15. Review Queue
CREATE TABLE IF NOT EXISTS review_queue (
    id TEXT PRIMARY KEY,
    raw_text TEXT NOT NULL,
    parsed_result TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    issue_reason TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING',
    approved_transaction_id TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (approved_transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_review_queue_status ON review_queue(status);

-- 16. Credit Cards & Credit Lines
CREATE TABLE IF NOT EXISTS credit_cards (
    id TEXT PRIMARY KEY,
    account_id TEXT,
    name TEXT NOT NULL,
    bank_name TEXT NOT NULL,
    credit_limit REAL NOT NULL DEFAULT 0.0,
    current_balance REAL NOT NULL DEFAULT 0.0,
    billing_cycle_day INTEGER NOT NULL CHECK (billing_cycle_day BETWEEN 1 AND 31),
    payment_due_day INTEGER NOT NULL CHECK (payment_due_day BETWEEN 1 AND 31),
    is_active INTEGER NOT NULL DEFAULT 1,
    credit_type TEXT NOT NULL DEFAULT 'CREDIT_CARD',
    provider TEXT DEFAULT NULL,
    billing_model TEXT NOT NULL DEFAULT 'STATEMENT_CYCLE',
    icon TEXT DEFAULT 'credit-card',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL
);

-- 16b. Credit Line Installments (PayLater per-transaction installment schedule)
CREATE TABLE IF NOT EXISTS credit_line_installments (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    transaction_id TEXT,
    description TEXT NOT NULL,
    original_amount REAL NOT NULL CHECK (original_amount > 0),
    remaining_amount REAL NOT NULL CHECK (remaining_amount >= 0),
    monthly_installment REAL NOT NULL CHECK (monthly_installment > 0),
    tenor_months INTEGER NOT NULL CHECK (tenor_months > 0),
    remaining_tenor INTEGER NOT NULL CHECK (remaining_tenor >= 0),
    interest_rate_annual REAL NOT NULL DEFAULT 0.0,
    admin_fee REAL NOT NULL DEFAULT 0.0,
    start_date TEXT NOT NULL,
    next_due_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (card_id) REFERENCES credit_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_cli_card ON credit_line_installments(card_id);
CREATE INDEX IF NOT EXISTS idx_cli_status ON credit_line_installments(status);

-- 17. Credit Card Statements
CREATE TABLE IF NOT EXISTS credit_card_statements (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    statement_period TEXT NOT NULL,
    statement_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    total_amount REAL NOT NULL DEFAULT 0.0,
    minimum_payment REAL NOT NULL DEFAULT 0.0,
    unpaid_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'UNPAID',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (card_id) REFERENCES credit_cards(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_cc_statements_card ON credit_card_statements(card_id);

-- 18. Credit Card Payments
CREATE TABLE IF NOT EXISTS credit_card_payments (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    statement_id TEXT,
    transaction_id TEXT,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (card_id) REFERENCES credit_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (statement_id) REFERENCES credit_card_statements(id) ON DELETE SET NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_cc_payments_card ON credit_card_payments(card_id);

-- 19. Liability Payments
CREATE TABLE IF NOT EXISTS liability_payments (
    id TEXT PRIMARY KEY,
    liability_id TEXT NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    principal_portion REAL NOT NULL DEFAULT 0.0,
    interest_portion REAL NOT NULL DEFAULT 0.0,
    transaction_id TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (liability_id) REFERENCES liabilities(id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_liability_payments_liab ON liability_payments(liability_id);

-- 20. Asset Valuation History
CREATE TABLE IF NOT EXISTS asset_valuation_history (
    id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    valuation_date TEXT NOT NULL,
    value REAL NOT NULL CHECK (value >= 0),
    reason TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_asset_valuation_asset ON asset_valuation_history(asset_id);

-- 21. Transaction Archive
CREATE TABLE IF NOT EXISTS transaction_archive (
    id TEXT PRIMARY KEY,
    original_id TEXT,
    amount REAL,
    date TEXT,
    direction TEXT,
    account_id TEXT,
    category_id TEXT,
    subcategory_id TEXT,
    note TEXT,
    source TEXT,
    status TEXT,
    reason TEXT,
    archived_at TEXT,
    raw_payload TEXT
);
-- 22. Processed Emails (Gmail Finance Intelligence)
CREATE TABLE IF NOT EXISTS processed_emails (
    message_id TEXT PRIMARY KEY,
    thread_id TEXT,
    sender TEXT NOT NULL,
    subject TEXT NOT NULL,
    received_date TEXT,
    fingerprint TEXT,
    status TEXT NOT NULL DEFAULT 'PROCESSED',
    review_item_id TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (review_item_id) REFERENCES review_queue(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_processed_emails_fingerprint ON processed_emails(fingerprint);
CREATE INDEX IF NOT EXISTS idx_processed_emails_review ON processed_emails(review_item_id);

-- 23. Credit Line Installments (PayLater per-transaction installment schedule)
CREATE TABLE IF NOT EXISTS credit_line_installments (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    transaction_id TEXT,
    description TEXT NOT NULL,
    original_amount REAL NOT NULL CHECK (original_amount > 0),
    remaining_amount REAL NOT NULL CHECK (remaining_amount >= 0),
    monthly_installment REAL NOT NULL CHECK (monthly_installment > 0),
    tenor_months INTEGER NOT NULL CHECK (tenor_months > 0),
    remaining_tenor INTEGER NOT NULL CHECK (remaining_tenor >= 0),
    interest_rate_annual REAL NOT NULL DEFAULT 0.0,
    admin_fee REAL NOT NULL DEFAULT 0.0,
    start_date TEXT NOT NULL,
    next_due_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (card_id) REFERENCES credit_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_cli_card ON credit_line_installments(card_id);
CREATE INDEX IF NOT EXISTS idx_cli_status ON credit_line_installments(status);

-- 24. Dedicated Financial Categories for Non-Operational Inflow & Debt Expenses
INSERT OR IGNORE INTO categories (id, name, is_active, keywords) 
VALUES ('cat_loan_disbursement', 'Pencairan Pinjaman', 1, 'pinjaman,disbursement,hutang');

INSERT OR IGNORE INTO categories (id, name, is_active, keywords) 
VALUES ('cat_loan_interest', 'Bunga & Biaya Pinjaman', 1, 'bunga,fee,admin,pinjaman');

INSERT OR IGNORE INTO categories (id, name, is_active, keywords) 
VALUES ('cat_late_fee', 'Denda & Biaya Keterlambatan', 1, 'denda,late fee,penalti');
