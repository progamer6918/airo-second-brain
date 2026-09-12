import os
import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from .db import DatabaseManager

@dataclass
class MonthlySummary:
    period: str  # YYYY-MM
    total_income: float
    total_expense: float
    net_cashflow: float
    transaction_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class CategorySpendingItem:
    category_id: Optional[str]
    category_name: str
    total_amount: float
    percentage: float
    transaction_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class CategorySpendingReport:
    period: str  # YYYY-MM
    total_expense: float
    categories: List[CategorySpendingItem]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period,
            "total_expense": self.total_expense,
            "categories": [c.to_dict() for c in self.categories]
        }

@dataclass
class AccountBalanceItem:
    account_id: str
    account_name: str
    account_type: str
    balance: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AccountOverview:
    total_liquid_balance: float
    account_count: int
    accounts: List[AccountBalanceItem]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_liquid_balance": self.total_liquid_balance,
            "account_count": self.account_count,
            "accounts": [a.to_dict() for a in self.accounts]
        }

@dataclass
class RecentActivityItem:
    transaction_id: str
    date: str
    account_id: str
    account_name: str
    category_id: Optional[str]
    category_name: str
    amount: float
    direction: str
    note: Optional[str]
    source: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SpendingAnomaly:
    anomaly_type: str  # LARGE_EXPENSE, CATEGORY_DOMINANCE, BUDGET_OVERRUN
    description: str
    metric_value: float
    threshold_value: float
    reference_id: Optional[str] = None
    category_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class FinanceInsightsService:
    """
    Read-Only Intelligence Layer on top of Finance Core.
    STRICT DATA BOUNDARY: All queries in this class are SELECT only.
    Zero mutations to ledger, zero LLM hallucinations, pure deterministic facts.
    """
    def __init__(self, db: DatabaseManager):
        self.db = db

    def _format_period(self, year: Optional[int] = None, month: Optional[int] = None) -> str:
        today = date.today()
        y = year if year is not None else today.year
        m = month if month is not None else today.month
        return f"{y:04d}-{m:02d}"

    # ----------------------------------------------------
    # A. Monthly Summary
    # ----------------------------------------------------
    def get_monthly_summary(self, year: Optional[int] = None, month: Optional[int] = None) -> MonthlySummary:
        period_str = self._format_period(year, month)
        conn = self.db.get_connection()
        
        query = """
            SELECT 
                direction, 
                COALESCE(SUM(amount), 0.0) as total_amount,
                COUNT(*) as tx_count
            FROM transactions
            WHERE substr(date, 1, 7) = ?
            GROUP BY direction
        """
        cur = conn.execute(query, (period_str,))
        rows = cur.fetchall()
        
        total_income = 0.0
        total_expense = 0.0
        total_count = 0
        
        for r in rows:
            d = r["direction"]
            amt = float(r["total_amount"])
            cnt = int(r["tx_count"])
            total_count += cnt
            if d == "INCOME":
                total_income += amt
            elif d == "EXPENSE":
                total_expense += amt

        net_cashflow = total_income - total_expense
        
        return MonthlySummary(
            period=period_str,
            total_income=total_income,
            total_expense=total_expense,
            net_cashflow=net_cashflow,
            transaction_count=total_count
        )

    # ----------------------------------------------------
    # B. Category Spending
    # ----------------------------------------------------
    def get_category_spending(self, year: Optional[int] = None, month: Optional[int] = None) -> CategorySpendingReport:
        period_str = self._format_period(year, month)
        conn = self.db.get_connection()

        # Get total expense for period
        tot_query = """
            SELECT COALESCE(SUM(amount), 0.0) as total_expense
            FROM transactions
            WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE'
        """
        tot_row = conn.execute(tot_query, (period_str,)).fetchone()
        total_expense = float(tot_row["total_expense"]) if tot_row else 0.0

        # Query group by category
        query = """
            SELECT 
                t.category_id,
                COALESCE(c.name, 'Lainnya / Tanpa Kategori') as category_name,
                COALESCE(SUM(t.amount), 0.0) as cat_total,
                COUNT(*) as cat_tx_count
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE substr(t.date, 1, 7) = ? AND t.direction = 'EXPENSE'
            GROUP BY t.category_id
            ORDER BY cat_total DESC
        """
        cur = conn.execute(query, (period_str,))
        rows = cur.fetchall()

        categories = []
        for r in rows:
            amt = float(r["cat_total"])
            pct = round((amt / total_expense * 100.0), 2) if total_expense > 0 else 0.0
            categories.append(
                CategorySpendingItem(
                    category_id=r["category_id"],
                    category_name=r["category_name"],
                    total_amount=amt,
                    percentage=pct,
                    transaction_count=int(r["cat_tx_count"])
                )
            )

        return CategorySpendingReport(
            period=period_str,
            total_expense=total_expense,
            categories=categories
        )

    # ----------------------------------------------------
    # C. Account Overview
    # ----------------------------------------------------
    def get_account_overview(self) -> AccountOverview:
        conn = self.db.get_connection()
        query = "SELECT id, name, type, balance FROM accounts ORDER BY name"
        cur = conn.execute(query)
        rows = cur.fetchall()

        items = []
        total_balance = 0.0
        for r in rows:
            bal = float(r["balance"])
            total_balance += bal
            items.append(
                AccountBalanceItem(
                    account_id=r["id"],
                    account_name=r["name"],
                    account_type=r["type"],
                    balance=bal
                )
            )

        return AccountOverview(
            total_liquid_balance=total_balance,
            account_count=len(items),
            accounts=items
        )

    # ----------------------------------------------------
    # D. Recent Activity
    # ----------------------------------------------------
    def get_recent_activity(self, limit: int = 10) -> List[RecentActivityItem]:
        conn = self.db.get_connection()
        query = """
            SELECT 
                t.id as tx_id,
                t.date,
                t.account_id,
                COALESCE(a.name, 'Akun Tidak Dikenal') as account_name,
                t.category_id,
                COALESCE(c.name, 'Lainnya') as category_name,
                t.amount,
                t.direction,
                t.note,
                t.source,
                t.created_at
            FROM transactions t
            LEFT JOIN accounts a ON t.account_id = a.id
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.created_at DESC, t.id DESC
            LIMIT ?
        """
        cur = conn.execute(query, (limit,))
        rows = cur.fetchall()

        activities = []
        for r in rows:
            activities.append(
                RecentActivityItem(
                    transaction_id=r["tx_id"],
                    date=r["date"],
                    account_id=r["account_id"],
                    account_name=r["account_name"],
                    category_id=r["category_id"],
                    category_name=r["category_name"],
                    amount=float(r["amount"]),
                    direction=r["direction"],
                    note=r["note"],
                    source=r["source"],
                    created_at=r["created_at"]
                )
            )

        return activities

    # ----------------------------------------------------
    # E. Spending Anomaly Candidate (Deterministic)
    # ----------------------------------------------------
    def get_spending_anomalies(self, year: Optional[int] = None, month: Optional[int] = None, multiplier: float = 2.5) -> List[SpendingAnomaly]:
        period_str = self._format_period(year, month)
        conn = self.db.get_connection()
        anomalies: List[SpendingAnomaly] = []

        # 1. Detect Large Single Expense (> multiplier * mean expense)
        stats_query = """
            SELECT 
                AVG(amount) as avg_amount,
                COUNT(*) as tx_count
            FROM transactions
            WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE'
        """
        stats_row = conn.execute(stats_query, (period_str,)).fetchone()
        if stats_row and stats_row["tx_count"] and int(stats_row["tx_count"]) >= 3:
            avg_exp = float(stats_row["avg_amount"])
            threshold = avg_exp * multiplier
            
            large_query = """
                SELECT id, amount, note, date
                FROM transactions
                WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE' AND amount >= ?
                ORDER BY amount DESC
            """
            for r in conn.execute(large_query, (period_str, threshold)).fetchall():
                anomalies.append(
                    SpendingAnomaly(
                        anomaly_type="LARGE_EXPENSE",
                        description=f"Pengeluaran tunggal ({r['note'] or 'Transaksi'}) sebesar Rp{r['amount']:,.0f} melebihi batas anomali (>{multiplier}x rata-rata bulanan Rp{avg_exp:,.0f}).",
                        metric_value=float(r["amount"]),
                        threshold_value=threshold,
                        reference_id=r["id"]
                    )
                )

        # 2. Detect Category Concentration (> 60% of total expenses when >= 2 categories exist)
        cat_report = self.get_category_spending(year, month)
        if cat_report.total_expense > 0 and len(cat_report.categories) >= 2:
            for cat in cat_report.categories:
                if cat.percentage >= 60.0:
                    anomalies.append(
                        SpendingAnomaly(
                            anomaly_type="CATEGORY_DOMINANCE",
                            description=f"Kategori '{cat.category_name}' mendominasi {cat.percentage}% dari total seluruh pengeluaran bulan ini (Rp{cat.total_amount:,.0f} dari Rp{cat_report.total_expense:,.0f}).",
                            metric_value=cat.percentage,
                            threshold_value=60.0,
                            category_name=cat.category_name
                        )
                    )

        # 3. Detect Budget Overrun from budgets table
        budget_query = """
            SELECT 
                b.id as budget_id,
                b.category_id,
                COALESCE(c.name, 'Kategori') as category_name,
                b.limit_amount
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE b.month = ?
        """
        try:
            cur = conn.execute(budget_query, (period_str,))
            for b in cur.fetchall():
                cat_match = next((c for c in cat_report.categories if c.category_id == b["category_id"]), None)
                actual_spent = cat_match.total_amount if cat_match else 0.0
                limit_amt = float(b["limit_amount"])
                if limit_amt > 0 and actual_spent > limit_amt:
                    anomalies.append(
                        SpendingAnomaly(
                            anomaly_type="BUDGET_OVERRUN",
                            description=f"Kategori '{b['category_name']}' melebihi batas anggaran bulanan: Rp{actual_spent:,.0f} terpakai (Limit: Rp{limit_amt:,.0f}).",
                            metric_value=actual_spent,
                            threshold_value=limit_amt,
                            reference_id=b["budget_id"],
                            category_name=b["category_name"]
                        )
                    )
        except sqlite3.OperationalError:
            pass

        return anomalies

    def get_full_insights_overview(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        Consolidated read model combining all five perspectives for fast, single-call consumption.
        """
        summary = self.get_monthly_summary(year, month)
        cat_spending = self.get_category_spending(year, month)
        accounts = self.get_account_overview()
        recent = self.get_recent_activity(limit=10)
        anomalies = self.get_spending_anomalies(year, month)

        return {
            "period": summary.period,
            "monthly_summary": summary.to_dict(),
            "category_spending": cat_spending.to_dict(),
            "account_overview": accounts.to_dict(),
            "recent_activity": [r.to_dict() for r in recent],
            "anomalies": [a.to_dict() for a in anomalies]
        }
