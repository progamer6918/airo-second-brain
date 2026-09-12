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
    created_at: Optional[str] = None

@dataclass
class Category:
    id: str
    name: str
    created_at: Optional[str] = None

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
