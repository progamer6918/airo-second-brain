from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

@dataclass
class Account:
    id: str
    name: str
    type: str
    balance: float = 0.0
    is_active: int = 1
    created_at: Optional[str] = None
    provider: Optional[str] = None
    account_class: str = 'LIQUID'
    dashboard_group: str = 'CASH'
    parent_account_id: Optional[str] = None
    aliases: str = ""

@dataclass
class Category:
    id: str
    name: str
    is_active: int = 1
    keywords: str = ""
    created_at: Optional[str] = None
    dashboard_group: str = 'GENERAL'
    domain: str = 'PERSONAL'
    event_type: str = 'REGULAR'

@dataclass
class Transaction:
    id: str
    date: str
    account_id: str
    amount: float
    direction: str
    category_id: Optional[str] = None
    note: Optional[str] = None
    source: str = 'MANUAL'
    created_at: Optional[str] = None
    subcategory_id: Optional[str] = None
    status: str = 'ACTIVE'
    voided_at: Optional[str] = None
    void_reason: Optional[str] = None
    updated_at: Optional[str] = None
    running_balance: Optional[float] = None

@dataclass
class Budget:
    id: str
    category_id: str
    month: str
    limit_amount: float
    created_at: Optional[str] = None

@dataclass
class AuditLog:
    id: str
    entity: str
    entity_id: str
    action: str
    created_at: Optional[str] = None

@dataclass
class FixedObligation:
    id: str
    name: str
    amount: float
    due_day: int
    category_id: Optional[str] = None
    is_active: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class FinanceConfig:
    key: str
    value: str
    updated_at: Optional[str] = None

@dataclass
class OwnerSession:
    id: str
    token_hash: str
    device_name: str
    created_at: str
    expires_at: str
    last_used_at: str
    revoked_at: Optional[str] = None

@dataclass
class Asset:
    id: str
    name: str
    type: str
    current_value: float
    notes: Optional[str] = None
    is_active: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    asset_class: str = "OTHER"
    weight_grams: float = 0.0
    purchase_cost: float = 0.0
    average_cost_per_gram: float = 0.0
    current_unit_price: float = 0.0

    @property
    def quantity_gram(self) -> float:
        return self.weight_grams

    @property
    def current_market_price(self) -> float:
        return self.current_unit_price

    @property
    def unrealized_gain_loss(self) -> float:
        return round(self.current_value - self.purchase_cost, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "current_value": self.current_value,
            "notes": self.notes,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "asset_class": self.asset_class,
            "weight_grams": self.weight_grams,
            "quantity_gram": self.quantity_gram,
            "purchase_cost": self.purchase_cost,
            "average_cost_per_gram": self.average_cost_per_gram,
            "current_unit_price": self.current_unit_price,
            "current_market_price": self.current_market_price,
            "unrealized_gain_loss": self.unrealized_gain_loss
        }

@dataclass
class Liability:
    id: str
    name: str
    type: str
    original_amount: float
    remaining_amount: float
    monthly_payment: float
    due_day: int
    notes: Optional[str] = None
    is_active: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class NetWorthReport:
    as_of_date: str
    total_liquid_balance: float
    total_assets_value: float
    total_liabilities_remaining: float
    net_worth: float
    active_accounts_count: int
    active_assets_count: int
    active_liabilities_count: int
    monthly_liability_payments: float

    def to_dict(self) -> dict:
        return {
            "as_of_date": self.as_of_date,
            "total_liquid_balance": self.total_liquid_balance,
            "total_assets_value": self.total_assets_value,
            "total_liabilities_remaining": self.total_liabilities_remaining,
            "net_worth": self.net_worth,
            "active_accounts_count": self.active_accounts_count,
            "active_assets_count": self.active_assets_count,
            "active_liabilities_count": self.active_liabilities_count,
            "monthly_liability_payments": self.monthly_liability_payments
        }

@dataclass
class Subcategory:
    id: str
    category_id: str
    name: str
    display_order: int = 0
    is_active: int = 1
    created_at: Optional[str] = None

@dataclass
class CategoryAlias:
    id: str
    keyword: str
    subcategory_id: Optional[str] = None
    category_id: Optional[str] = None
    priority: int = 10
    created_at: Optional[str] = None

@dataclass
class TransactionMetadata:
    transaction_id: str
    subcategory_id: Optional[str] = None
    raw_input: Optional[str] = None
    source_type: str = 'MANUAL'
    confidence_score: float = 1.0
    created_at: Optional[str] = None

@dataclass
class CorrectionEvent:
    id: str
    transaction_id: str
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class ReviewQueueItem:
    id: str
    raw_text: str
    parsed_result: str
    confidence: float = 1.0
    issue_reason: Optional[str] = None
    status: str = 'PENDING'
    approved_transaction_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class CreditCard:
    id: str
    name: str
    bank_name: str
    account_id: Optional[str] = None
    credit_limit: float = 0.0
    current_balance: float = 0.0
    billing_cycle_day: int = 1
    payment_due_day: int = 15
    is_active: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class CreditCardStatement:
    id: str
    card_id: str
    statement_period: str
    statement_date: str
    due_date: str
    total_amount: float = 0.0
    minimum_payment: float = 0.0
    unpaid_amount: float = 0.0
    status: str = 'UNPAID'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class CreditCardPayment:
    id: str
    card_id: str
    payment_date: str
    amount: float
    statement_id: Optional[str] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class LiabilityPayment:
    id: str
    liability_id: str
    payment_date: str
    amount: float
    principal_portion: float = 0.0
    interest_portion: float = 0.0
    transaction_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class AssetValuation:
    id: str
    asset_id: str
    valuation_date: str
    value: float
    reason: Optional[str] = None
    created_at: Optional[str] = None



def __getattr__(name: str):
    if name in ("WeeklyRecapReport", "LargestExpenseItem", "DailySpendingItem"):
        from .insights import WeeklyRecapReport, LargestExpenseItem, DailySpendingItem
        mapping = {
            "WeeklyRecapReport": WeeklyRecapReport,
            "LargestExpenseItem": LargestExpenseItem,
            "DailySpendingItem": DailySpendingItem,
        }
        return mapping[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


