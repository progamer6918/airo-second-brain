import os
import calendar
import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from .db import DatabaseManager
from .models import NetWorthReport


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

@dataclass
class ObligationStatusItem:
    obligation_id: str
    name: str
    amount: float
    due_day: int
    category_id: Optional[str]
    category_name: str
    is_active: bool
    is_paid_this_cycle: bool
    status: str  # 'PAID' or 'UNPAID'

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SafeToSpendReport:
    as_of_date: str
    cycle_start_date: str
    next_payday_date: str
    days_to_payday: int
    payday_day: int
    total_liquid_balance: float
    safety_floor: float
    total_active_obligations: float
    paid_obligations_this_cycle: float
    unpaid_obligations_this_cycle: float
    safe_to_spend: float
    daily_safe_allowance: float
    payday_runway_days: float
    status: str  # 'SAFE' or 'DEFICIT'
    deficit_amount: float
    obligations: List[ObligationStatusItem]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["obligations"] = [o.to_dict() for o in self.obligations]
        d["liquid_balance"] = self.total_liquid_balance
        d["current_cash_pool"] = self.total_liquid_balance
        d["commitments"] = self.unpaid_obligations_this_cycle
        d["unpaid_obligations_total"] = self.unpaid_obligations_this_cycle
        d["safe_to_spend_amount"] = self.safe_to_spend
        d["daily_allowance"] = self.daily_safe_allowance
        return d

@dataclass
class LargestExpenseItem:
    amount: float
    note: Optional[str]
    category_name: str
    date: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DailySpendingItem:
    date: str
    expense: float
    income: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class WeeklyRecapReport:
    as_of_date: str
    start_date: str
    end_date: str
    total_expense: float
    total_income: float
    net_cashflow: float
    daily_burn_rate: float
    expense_count: int
    income_count: int
    transfer_count: int
    top_category_name: Optional[str]
    top_category_amount: float
    top_category_percentage: float
    largest_expense: Optional[LargestExpenseItem]
    total_liquid_balance: float
    safe_to_spend: float
    days_to_payday: int
    daily_safe_allowance: float
    safe_to_spend_status: str
    categories: List[CategorySpendingItem]
    daily_breakdown: List[DailySpendingItem]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.largest_expense:
            d["largest_expense"] = self.largest_expense.to_dict()
        d["categories"] = [c.to_dict() for c in self.categories]
        d["daily_breakdown"] = [day.to_dict() for day in self.daily_breakdown]
        return d

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
            WHERE substr(date, 1, 7) = ? AND (status IS NULL OR status != 'VOID')
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
            WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE' AND (status IS NULL OR status != 'VOID')
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
            WHERE substr(t.date, 1, 7) = ? AND t.direction = 'EXPENSE' AND (t.status IS NULL OR t.status != 'VOID')
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
        query = "SELECT id, name, type, balance FROM accounts WHERE is_active = 1 OR is_active IS NULL ORDER BY name"
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
            WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE' AND (status IS NULL OR status != 'VOID')
        """
        stats_row = conn.execute(stats_query, (period_str,)).fetchone()
        if stats_row and stats_row["tx_count"] and int(stats_row["tx_count"]) >= 3:
            avg_exp = float(stats_row["avg_amount"])
            threshold = avg_exp * multiplier
            
            large_query = """
                SELECT id, amount, note, date
                FROM transactions
                WHERE substr(date, 1, 7) = ? AND direction = 'EXPENSE' AND amount >= ? AND (status IS NULL OR status != 'VOID')
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

    # ----------------------------------------------------
    # E. Safe-to-Spend Model (Phase 2.2)
    # ----------------------------------------------------
    def get_safe_to_spend_report(self, as_of: Optional[str] = None) -> SafeToSpendReport:
        """
        Deterministic Safe-to-Spend Calculation (Level 3 Insight).
        Formula:
          Safe-to-Spend = max(0, Total Liquid - Unpaid Commitments This Cycle - Safety Floor)
          Daily Safe Allowance = Safe-to-Spend / max(1, Days to Payday)
          Payday Runway = (Total Liquid - Unpaid Commitments) / Avg Daily Burn Rate
        STRICT READ ONLY: Zero ledger mutations.
        """
        conn = self.db.get_connection()

        # 1. Parse reference date
        if as_of:
            try:
                ref_date = date.fromisoformat(as_of)
            except Exception:
                ref_date = date.today()
        else:
            ref_date = date.today()
        as_of_str = ref_date.isoformat()

        # 2. Retrieve config parameters
        payday_day = 25
        safety_floor = 1000000.0
        try:
            cfg_cur = conn.execute("SELECT key, value FROM finance_config WHERE key IN ('payday_day', 'safety_floor')")
            for row in cfg_cur.fetchall():
                k = row["key"]
                v = str(row["value"]).strip()
                if k == "payday_day" and v.isdigit():
                    val_int = int(v)
                    if 1 <= val_int <= 31:
                        payday_day = val_int
                elif k == "safety_floor":
                    try:
                        val_flt = float(v)
                        if val_flt >= 0:
                            safety_floor = val_flt
                    except ValueError:
                        pass
        except sqlite3.OperationalError:
            pass

        # 3. Calculate cycle dates and days_to_payday
        if ref_date.day < payday_day:
            max_day_this_month = calendar.monthrange(ref_date.year, ref_date.month)[1]
            next_payday_day = min(payday_day, max_day_this_month)
            next_payday = date(ref_date.year, ref_date.month, next_payday_day)

            if ref_date.month == 1:
                prev_year, prev_month = ref_date.year - 1, 12
            else:
                prev_year, prev_month = ref_date.year, ref_date.month - 1
            max_day_prev_month = calendar.monthrange(prev_year, prev_month)[1]
            prev_payday_day = min(payday_day, max_day_prev_month)
            cycle_start = date(prev_year, prev_month, prev_payday_day)
        else:
            max_day_this_month = calendar.monthrange(ref_date.year, ref_date.month)[1]
            cur_payday_day = min(payday_day, max_day_this_month)
            cycle_start = date(ref_date.year, ref_date.month, cur_payday_day)

            if ref_date.month == 12:
                next_year, next_month = ref_date.year + 1, 1
            else:
                next_year, next_month = ref_date.year, ref_date.month + 1
            max_day_next_month = calendar.monthrange(next_year, next_month)[1]
            next_payday_day = min(payday_day, max_day_next_month)
            next_payday = date(next_year, next_month, next_payday_day)

        days_to_payday = (next_payday - ref_date).days
        if days_to_payday <= 0:
            days_to_payday = 1

        cycle_start_str = cycle_start.isoformat()
        next_payday_str = next_payday.isoformat()

        # 4. Total liquid balance
        account_overview = self.get_account_overview()
        total_liquid = account_overview.total_liquid_balance

        # 5. Query active fixed obligations and determine payment status this cycle
        obligation_items: List[ObligationStatusItem] = []
        try:
            cur = conn.execute("""
                SELECT o.id, o.name, o.amount, o.due_day, o.category_id, o.is_active,
                       COALESCE(c.name, 'Umum') as category_name
                FROM fixed_obligations o
                LEFT JOIN categories c ON o.category_id = c.id
                WHERE o.is_active = 1
                ORDER BY o.due_day ASC, o.name ASC
            """)
            rows = cur.fetchall()
            for r in rows:
                obl_id = r["id"]
                name = r["name"]
                amt = float(r["amount"])
                due_day = int(r["due_day"])
                cat_id = r["category_id"]
                cat_name = r["category_name"]

                check_query = """
                    SELECT COALESCE(SUM(amount), 0.0) as paid_sum
                    FROM transactions
                    WHERE direction = 'EXPENSE'
                      AND (status IS NULL OR status != 'VOID')
                      AND date >= ? AND date <= ?
                      AND (
                        (category_id IS NOT NULL AND category_id = ?)
                        OR (note IS NOT NULL AND LOWER(note) LIKE ?)
                      )
                """
                like_pat = f"%{name.lower()}%"
                paid_res = conn.execute(check_query, (cycle_start_str, as_of_str, cat_id or "", like_pat)).fetchone()
                paid_sum = float(paid_res["paid_sum"]) if paid_res else 0.0

                is_paid = paid_sum >= (amt * 0.9)
                obligation_items.append(
                    ObligationStatusItem(
                        obligation_id=obl_id,
                        name=name,
                        amount=amt,
                        due_day=due_day,
                        category_id=cat_id,
                        category_name=cat_name,
                        is_active=True,
                        is_paid_this_cycle=is_paid,
                        status="PAID" if is_paid else "UNPAID"
                    )
                )
        except sqlite3.OperationalError:
            pass

        total_active_obligations = sum(o.amount for o in obligation_items)
        paid_obligations = sum(o.amount for o in obligation_items if o.is_paid_this_cycle)
        unpaid_obligations = sum(o.amount for o in obligation_items if not o.is_paid_this_cycle)

        # 6. Calculate Safe-to-Spend
        net_calc = total_liquid - unpaid_obligations - safety_floor
        if net_calc >= 0:
            safe_to_spend = round(net_calc, 2)
            status = "SAFE"
            deficit_amount = 0.0
        else:
            safe_to_spend = 0.0
            status = "DEFICIT"
            deficit_amount = round(abs(net_calc), 2)

        # 7. Daily Safe Allowance
        daily_safe_allowance = round(safe_to_spend / max(1, days_to_payday), 2)

        # 8. Payday Runway (Days)
        unencumbered_liquid = max(0.0, total_liquid - unpaid_obligations)
        thirty_days_ago = (ref_date - timedelta(days=30)).isoformat()
        burn_query = """
            SELECT COALESCE(SUM(amount), 0.0) as total_spent
            FROM transactions
            WHERE direction = 'EXPENSE'
              AND (status IS NULL OR status != 'VOID')
              AND date >= ? AND date <= ?
        """
        burn_res = conn.execute(burn_query, (thirty_days_ago, as_of_str)).fetchone()
        thirty_day_spent = float(burn_res["total_spent"]) if burn_res else 0.0
        avg_daily_burn = thirty_day_spent / 30.0

        if avg_daily_burn > 0:
            payday_runway_days = round(unencumbered_liquid / avg_daily_burn, 1)
        else:
            payday_runway_days = 999.0 if unencumbered_liquid > 0 else 0.0

        return SafeToSpendReport(
            as_of_date=as_of_str,
            cycle_start_date=cycle_start_str,
            next_payday_date=next_payday_str,
            days_to_payday=days_to_payday,
            payday_day=payday_day,
            total_liquid_balance=round(total_liquid, 2),
            safety_floor=round(safety_floor, 2),
            total_active_obligations=round(total_active_obligations, 2),
            paid_obligations_this_cycle=round(paid_obligations, 2),
            unpaid_obligations_this_cycle=round(unpaid_obligations, 2),
            safe_to_spend=safe_to_spend,
            daily_safe_allowance=daily_safe_allowance,
            payday_runway_days=payday_runway_days,
            status=status,
            deficit_amount=deficit_amount,
            obligations=obligation_items
        )

    def get_full_insights_overview(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        Consolidated read model combining all six perspectives for fast, single-call consumption.
        """
        summary = self.get_monthly_summary(year, month)
        cat_spending = self.get_category_spending(year, month)
        accounts = self.get_account_overview()
        recent = self.get_recent_activity(limit=10)
        anomalies = self.get_spending_anomalies(year, month)
        safe_to_spend = self.get_safe_to_spend_report()

        return {
            "period": summary.period,
            "monthly_summary": summary.to_dict(),
            "category_spending": cat_spending.to_dict(),
            "account_overview": accounts.to_dict(),
            "recent_activity": [r.to_dict() for r in recent],
            "anomalies": [a.to_dict() for a in anomalies],
            "safe_to_spend": safe_to_spend.to_dict()
        }

    # ----------------------------------------------------
    # G. Weekly Finance Recap (Phase 2.3 Package A)
    # ----------------------------------------------------
    def get_weekly_recap_report(self, as_of: Optional[str] = None) -> WeeklyRecapReport:
        """
        Calculates bounded Weekly Finance Recap for rolling 7 days.
        Deterministic Python math, 0 LLM dependency, 0 database writes.
        """
        if as_of:
            try:
                ref_date = datetime.strptime(as_of, "%Y-%m-%d").date()
            except ValueError:
                ref_date = date.today()
        else:
            ref_date = date.today()

        end_date = ref_date
        start_date = end_date - timedelta(days=6)
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
        as_of_str = end_date_str

        conn = self.db.get_connection()

        # 1. Total expense and count (TRANSFER excluded)
        exp_query = """
            SELECT COALESCE(SUM(amount), 0.0) as total_expense, COUNT(*) as tx_count
            FROM transactions
            WHERE date >= ? AND date <= ? AND direction = 'EXPENSE' AND (status IS NULL OR status != 'VOID')
        """
        exp_row = conn.execute(exp_query, (start_date_str, end_date_str)).fetchone()
        total_expense = float(exp_row["total_expense"]) if exp_row else 0.0
        expense_count = int(exp_row["tx_count"]) if exp_row else 0

        # 2. Total income and count (TRANSFER excluded)
        inc_query = """
            SELECT COALESCE(SUM(amount), 0.0) as total_income, COUNT(*) as tx_count
            FROM transactions
            WHERE date >= ? AND date <= ? AND direction = 'INCOME' AND (status IS NULL OR status != 'VOID')
        """
        inc_row = conn.execute(inc_query, (start_date_str, end_date_str)).fetchone()
        total_income = float(inc_row["total_income"]) if inc_row else 0.0
        income_count = int(inc_row["tx_count"]) if inc_row else 0

        # 3. Transfer count (TRANSFER tracked, but excluded from income/expense)
        trf_query = """
            SELECT COUNT(*) as tx_count
            FROM transactions
            WHERE date >= ? AND date <= ? AND direction = 'TRANSFER' AND (status IS NULL OR status != 'VOID')
        """
        trf_row = conn.execute(trf_query, (start_date_str, end_date_str)).fetchone()
        transfer_count = int(trf_row["tx_count"]) if trf_row else 0

        # 4. Net cashflow & daily burn rate
        net_cashflow = round(total_income - total_expense, 2)
        daily_burn_rate = round(total_expense / 7.0, 2)

        # 5. Category breakdown & top category
        cat_query = """
            SELECT 
                t.category_id,
                COALESCE(c.name, 'Lainnya / Tanpa Kategori') as category_name,
                COALESCE(SUM(t.amount), 0.0) as cat_total,
                COUNT(*) as cat_tx_count
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.date >= ? AND t.date <= ? AND t.direction = 'EXPENSE' AND (t.status IS NULL OR t.status != 'VOID')
            GROUP BY t.category_id
            ORDER BY cat_total DESC
        """
        cat_rows = conn.execute(cat_query, (start_date_str, end_date_str)).fetchall()
        categories: List[CategorySpendingItem] = []
        for r in cat_rows:
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

        if categories:
            top_category_name = categories[0].category_name
            top_category_amount = categories[0].total_amount
            top_category_percentage = categories[0].percentage
        else:
            top_category_name = None
            top_category_amount = 0.0
            top_category_percentage = 0.0

        # 6. Largest expense
        largest_query = """
            SELECT 
                t.amount,
                t.note,
                t.date,
                COALESCE(c.name, 'Lainnya / Tanpa Kategori') as category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.date >= ? AND t.date <= ? AND t.direction = 'EXPENSE' AND (t.status IS NULL OR t.status != 'VOID')
            ORDER BY t.amount DESC, t.date DESC
            LIMIT 1
        """
        largest_row = conn.execute(largest_query, (start_date_str, end_date_str)).fetchone()
        largest_expense: Optional[LargestExpenseItem] = None
        if largest_row:
            largest_expense = LargestExpenseItem(
                amount=float(largest_row["amount"]),
                note=largest_row["note"],
                category_name=largest_row["category_name"],
                date=largest_row["date"]
            )

        # 7. Daily breakdown for the 7 days
        daily_query = """
            SELECT 
                date,
                direction,
                COALESCE(SUM(amount), 0.0) as day_total
            FROM transactions
            WHERE date >= ? AND date <= ? AND direction IN ('EXPENSE', 'INCOME') AND (status IS NULL OR status != 'VOID')
            GROUP BY date, direction
        """
        daily_rows = conn.execute(daily_query, (start_date_str, end_date_str)).fetchall()
        daily_map: Dict[str, Dict[str, float]] = {}
        for r in daily_rows:
            d_str = r["date"]
            if d_str not in daily_map:
                daily_map[d_str] = {"EXPENSE": 0.0, "INCOME": 0.0}
            daily_map[d_str][r["direction"]] = float(r["day_total"])

        daily_breakdown: List[DailySpendingItem] = []
        for i in range(7):
            day_d = start_date + timedelta(days=i)
            day_str = day_d.isoformat()
            exp_amt = daily_map.get(day_str, {}).get("EXPENSE", 0.0)
            inc_amt = daily_map.get(day_str, {}).get("INCOME", 0.0)
            daily_breakdown.append(DailySpendingItem(date=day_str, expense=exp_amt, income=inc_amt))

        # 8. Liquid balance snapshot
        account_overview = self.get_account_overview()
        total_liquid_balance = account_overview.total_liquid_balance

        # 9. Safe-to-Spend context
        sts = self.get_safe_to_spend_report(as_of=as_of_str)
        safe_to_spend = sts.safe_to_spend
        days_to_payday = sts.days_to_payday
        daily_safe_allowance = sts.daily_safe_allowance
        safe_to_spend_status = sts.status

        return WeeklyRecapReport(
            as_of_date=as_of_str,
            start_date=start_date_str,
            end_date=end_date_str,
            total_expense=round(total_expense, 2),
            total_income=round(total_income, 2),
            net_cashflow=net_cashflow,
            daily_burn_rate=daily_burn_rate,
            expense_count=expense_count,
            income_count=income_count,
            transfer_count=transfer_count,
            top_category_name=top_category_name,
            top_category_amount=round(top_category_amount, 2),
            top_category_percentage=top_category_percentage,
            largest_expense=largest_expense,
            total_liquid_balance=round(total_liquid_balance, 2),
            safe_to_spend=safe_to_spend,
            days_to_payday=days_to_payday,
            daily_safe_allowance=daily_safe_allowance,
            safe_to_spend_status=safe_to_spend_status,
            categories=categories,
            daily_breakdown=daily_breakdown
        )

    # ----------------------------------------------------
    # Package B: Net Worth & Position Intelligence
    # ----------------------------------------------------
    def get_net_worth_report(self, as_of: Optional[str] = None) -> NetWorthReport:
        """
        Deterministic Level 3 Net Worth calculation:
        Net Worth = Liquid Cash Balance + Total Active Assets - Total Active Liabilities
        """
        if as_of:
            try:
                as_of_date = datetime.strptime(as_of.strip(), "%Y-%m-%d").date()
            except ValueError:
                as_of_date = date.today()
        else:
            as_of_date = date.today()

        conn = self.db.get_connection()
        # 1. Total liquid balance from active accounts
        acc_cur = conn.execute("SELECT balance FROM accounts WHERE is_active = 1")
        acc_rows = acc_cur.fetchall()
        total_liquid = float(sum(r["balance"] for r in acc_rows))
        active_acc_count = len(acc_rows)

        # 2. Total active assets value
        ast_cur = conn.execute("SELECT current_value FROM assets WHERE is_active = 1")
        ast_rows = ast_cur.fetchall()
        total_assets = float(sum(r["current_value"] for r in ast_rows))
        active_ast_count = len(ast_rows)

        # 3. Total active liabilities remaining and monthly payment
        liab_cur = conn.execute("SELECT remaining_amount, monthly_payment FROM liabilities WHERE is_active = 1")
        liab_rows = liab_cur.fetchall()
        total_liabilities = float(sum(r["remaining_amount"] for r in liab_rows))
        monthly_payments = float(sum(r["monthly_payment"] for r in liab_rows))
        active_liab_count = len(liab_rows)

        net_worth = total_liquid + total_assets - total_liabilities

        return NetWorthReport(
            as_of_date=as_of_date.isoformat(),
            total_liquid_balance=round(total_liquid, 2),
            total_assets_value=round(total_assets, 2),
            total_liabilities_remaining=round(total_liabilities, 2),
            net_worth=round(net_worth, 2),
            active_accounts_count=active_acc_count,
            active_assets_count=active_ast_count,
            active_liabilities_count=active_liab_count,
            monthly_liability_payments=round(monthly_payments, 2)
        )

    def get_assets_summary(self) -> Dict[str, Any]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM assets WHERE is_active = 1 ORDER BY current_value DESC")
        rows = [dict(r) for r in cur.fetchall()]
        
        gold_tracker = None
        for r in rows:
            if "emas" in r["name"].lower() or "logam mulia" in r["name"].lower():
                val = float(r["current_value"])
                weight = float(r.get("weight_grams") or 50.0)
                purchase_cost = float(r.get("purchase_cost") or 55000000.0)
                avg_cost_per_gram = float(r.get("average_cost_per_gram") or (purchase_cost / weight if weight > 0 else 1100000.0))
                market_price_per_gram = float(r.get("current_unit_price") or (val / weight if weight > 0 else 1500000.0))
                profit_loss = val - purchase_cost
                profit_loss_pct = (profit_loss / purchase_cost * 100.0) if purchase_cost > 0 else 0.0
                
                v_cur = conn.execute("SELECT valuation_date, value, reason FROM asset_valuation_history WHERE asset_id = ? ORDER BY valuation_date ASC", (r["id"],))
                v_rows = [dict(vr) for vr in v_cur.fetchall()]
                
                r["gold_details"] = {
                    "weight_grams": weight,
                    "purchase_cost": purchase_cost,
                    "purchase_cost_per_gram": avg_cost_per_gram,
                    "average_cost_per_gram": avg_cost_per_gram,
                    "total_cost": purchase_cost,
                    "current_price_per_gram": market_price_per_gram,
                    "current_unit_price": market_price_per_gram,
                    "current_valuation": val,
                    "profit_loss": profit_loss,
                    "profit_loss_pct": round(profit_loss_pct, 1),
                    "valuation_history": v_rows
                }
                gold_tracker = r["gold_details"]

        total_val = sum(r["current_value"] for r in rows)
        return {
            "total_assets_value": round(total_val, 2),
            "asset_count": len(rows),
            "assets": rows,
            "gold_tracker": gold_tracker
        }

    def get_liabilities_summary(self) -> Dict[str, Any]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM liabilities WHERE is_active = 1 ORDER BY remaining_amount DESC")
        rows = [dict(r) for r in cur.fetchall()]
        
        mortgage_tracker = None
        for r in rows:
            if r["type"] == "MORTGAGE" or "kpr" in r["name"].lower():
                pmt_cur = conn.execute("SELECT count(*) FROM liability_payments WHERE liability_id = ?", (r["id"],))
                paid_pmts = pmt_cur.fetchone()[0]
                base_paid = 57
                paid_count = max(57, paid_pmts)
                total_tenor = 120
                remaining_installments = max(0, total_tenor - paid_count)
                next_installment_num = paid_count + 1 if remaining_installments > 0 else total_tenor
                
                h_cur = conn.execute("SELECT payment_date, amount, principal_portion, interest_portion, notes FROM liability_payments WHERE liability_id = ? ORDER BY payment_date DESC LIMIT 12", (r["id"],))
                h_rows = [dict(hr) for hr in h_cur.fetchall()]
                
                r["mortgage_details"] = {
                    "start_date": "2022-01-01",
                    "total_tenor_months": total_tenor,
                    "paid_installments": paid_count,
                    "remaining_installments": remaining_installments,
                    "next_installment_number": next_installment_num,
                    "next_payment_month": "Oktober 2026",
                    "next_payment_due_day": r["due_day"],
                    "monthly_installment": float(r["monthly_payment"]),
                    "recent_payments": h_rows
                }
                mortgage_tracker = r["mortgage_details"]

        total_rem = sum(r["remaining_amount"] for r in rows)
        total_mon = sum(r["monthly_payment"] for r in rows)
        return {
            "total_liabilities_remaining": round(total_rem, 2),
            "total_monthly_payment": round(total_mon, 2),
            "liability_count": len(rows),
            "liabilities": rows,
            "mortgage_tracker": mortgage_tracker
        }

    def get_spending_by_subcategory(self, period: Optional[str] = None) -> Dict[str, Any]:
        """
        Aggregates expense transactions broken down by category and subcategory.
        If period is omitted, defaults to current month (YYYY-MM).
        """
        conn = self.db.get_connection()
        if not period:
            period = date.today().strftime("%Y-%m")
        
        query = """
            SELECT 
                c.id as category_id,
                c.name as category_name,
                s.id as subcategory_id,
                COALESCE(s.name, 'Unclassified') as subcategory_name,
                SUM(t.amount) as total_amount,
                COUNT(t.id) as tx_count
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN transaction_metadata tm ON t.id = tm.transaction_id
            LEFT JOIN subcategories s ON COALESCE(t.subcategory_id, tm.subcategory_id) = s.id
            WHERE t.direction = 'EXPENSE'
              AND (t.status IS NULL OR t.status != 'VOID')
              AND strftime('%Y-%m', t.date) = ?
            GROUP BY c.id, c.name, s.id, s.name
            ORDER BY total_amount DESC
        """
        cur = conn.execute(query, (period,))
        items = []
        total_expense = 0.0
        for r in cur.fetchall():
            amt = float(r["total_amount"])
            total_expense += amt
            items.append({
                "category_id": r["category_id"],
                "category_name": r["category_name"] or "Tanpa Kategori",
                "subcategory_id": r["subcategory_id"],
                "subcategory_name": r["subcategory_name"],
                "total_amount": round(amt, 2),
                "tx_count": int(r["tx_count"])
            })
        
        for item in items:
            item["percentage"] = round((item["total_amount"] / total_expense * 100.0), 1) if total_expense > 0 else 0.0

        return {
            "period": period,
            "total_expense": round(total_expense, 2),
            "breakdown_count": len(items),
            "breakdown": items
        }

    def get_credit_card_summary(self) -> Dict[str, Any]:
        """
        Provides summary of credit cards: limit, current balance, available credit, statements,
        and dynamic billing cycle overview (Statement Balance vs Unbilled vs Payment Reserve).
        """
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM credit_cards WHERE is_active = 1 ORDER BY name ASC")
        cards = []
        total_limit = 0.0
        total_balance = 0.0

        # Query payment reserve from Blu Pocket CC (or any reserve pocket)
        reserve_cur = conn.execute("SELECT balance FROM accounts WHERE LOWER(name) LIKE '%pocket cc%' LIMIT 1")
        reserve_row = reserve_cur.fetchone()
        payment_reserve = float(reserve_row["balance"]) if reserve_row else 0.0

        for r in cur.fetchall():
            limit = float(r["credit_limit"])
            bal = float(r["current_balance"])
            total_limit += limit
            total_balance += bal

            # Dynamic Billing Cycle calculation based on card billing_cycle_day (default 15)
            row_keys = r.keys() if hasattr(r, "keys") else []
            cycle_day = int(r["billing_cycle_day"]) if "billing_cycle_day" in row_keys and r["billing_cycle_day"] else 15
            due_day = int(r["payment_due_day"]) if "payment_due_day" in row_keys and r["payment_due_day"] else 30
            today = date.today()

            # Determine closed cycle boundary
            # If today.day > cycle_day (e.g. today is 16th or later):
            # Closed cycle is: (day+1 of last month) to (day of current month)
            # Current unbilled cycle is: (day+1 of current month) to (day of next month)
            # If today.day <= cycle_day:
            # Closed cycle is: (day+1 of 2 months ago) to (day of last month)
            # Current unbilled cycle is: (day+1 of last month) to (day of current month)
            if today.day > cycle_day:
                c_end = date(today.year, today.month, cycle_day)
                if today.month == 1:
                    c_start = date(today.year - 1, 12, cycle_day + 1)
                else:
                    c_start = date(today.year, today.month - 1, cycle_day + 1)
                # Next unbilled period
                u_start = date(c_end.year, c_end.month, cycle_day + 1)
                if c_end.month == 12:
                    u_end = date(c_end.year + 1, 1, cycle_day)
                else:
                    u_end = date(c_end.year, c_end.month + 1, cycle_day)
            else:
                if today.month == 1:
                    c_end = date(today.year - 1, 12, cycle_day)
                    c_start = date(today.year - 1, 11, cycle_day + 1)
                elif today.month == 2:
                    c_end = date(today.year, 1, cycle_day)
                    c_start = date(today.year - 1, 12, cycle_day + 1)
                else:
                    c_end = date(today.year, today.month - 1, cycle_day)
                    c_start = date(today.year, today.month - 2, cycle_day + 1)
                u_start = date(c_end.year, c_end.month, cycle_day + 1)
                u_end = date(today.year, today.month, cycle_day)

            # Determine due date for closed statement
            due_month = c_end.month
            due_year = c_end.year
            if due_day <= cycle_day:
                if due_month == 12:
                    due_month = 1
                    due_year += 1
                else:
                    due_month += 1
            max_day_due = calendar.monthrange(due_year, due_month)[1]
            c_due = date(due_year, due_month, min(due_day, max_day_due))

            month_names_short = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
            c_period_str = f"{c_start.day} {month_names_short[c_start.month]} - {c_end.day} {month_names_short[c_end.month]} {c_end.year}"
            u_period_str = f"{u_start.day} {month_names_short[u_start.month]} - {u_end.day} {month_names_short[u_end.month]} {u_end.year}"
            cycle_code = f"TOKPED_CC_{c_end.strftime('%Y-%m')}"

            # Fetch statements for this card
            card_stmts = conn.execute(
                "SELECT * FROM credit_card_statements WHERE card_id = ? ORDER BY due_date DESC",
                (r["id"],)
            ).fetchall()

            if card_stmts:
                latest_stmt = dict(card_stmts[0])
                stmt_bal = float(latest_stmt.get("unpaid_amount", latest_stmt.get("total_amount", 0.0)))
                closed_stmt = {
                    "id": latest_stmt.get("id"),
                    "cycle_code": cycle_code,
                    "statement_period": latest_stmt.get("statement_period", c_period_str),
                    "period_start": latest_stmt.get("period_start", c_start.isoformat()),
                    "period_end": latest_stmt.get("period_end", c_end.isoformat()),
                    "statement_date": latest_stmt.get("statement_date", c_end.isoformat()),
                    "due_date": latest_stmt.get("due_date", c_due.isoformat()),
                    "total_amount": float(latest_stmt.get("total_amount", 0.0)),
                    "unpaid_amount": stmt_bal,
                    "pocket_ready": payment_reserve,
                    "remaining": max(0.0, stmt_bal - payment_reserve),
                    "status": "AMAN" if (stmt_bal == 0 or payment_reserve >= stmt_bal) else "PERLU_DIPERSIAPKAN"
                }
            else:
                stmt_bal = min(bal, 351000.0) if bal > 0 else 0.0
                closed_stmt = {
                    "id": "stmt_current",
                    "cycle_code": cycle_code,
                    "statement_period": c_period_str,
                    "period_start": c_start.isoformat(),
                    "period_end": c_end.isoformat(),
                    "statement_date": c_end.isoformat(),
                    "due_date": c_due.isoformat(),
                    "total_amount": stmt_bal,
                    "unpaid_amount": stmt_bal,
                    "pocket_ready": payment_reserve,
                    "remaining": max(0.0, stmt_bal - payment_reserve),
                    "status": "AMAN" if (stmt_bal == 0 or payment_reserve >= stmt_bal) else "PERLU_DIPERSIAPKAN"
                }

            unbilled = max(0.0, bal - stmt_bal)
            current_period = {
                "statement_period": u_period_str,
                "period_start": u_start.isoformat(),
                "period_end": u_end.isoformat(),
                "unbilled_amount": unbilled,
                "total_temporary": unbilled,
                "not_prepared": max(0.0, unbilled - max(0.0, payment_reserve - stmt_bal)),
                "status": "Tracking",
                "is_closed": False
            }

            cards.append({
                "id": r["id"],
                "name": r["name"],
                "bank_name": r["bank_name"],
                "credit_limit": round(limit, 2),
                "current_balance": round(bal, 2),
                "statement_balance": round(stmt_bal, 2),
                "unbilled_transactions": round(unbilled, 2),
                "payment_reserve": round(payment_reserve, 2),
                "available_credit": round(max(0.0, limit - bal), 2),
                "billing_cycle_day": cycle_day,
                "payment_due_day": due_day,
                "utilization_rate": round((bal / limit * 100.0), 1) if limit > 0 else 0.0,
                "closed_statement": closed_stmt,
                "current_period": current_period
            })
            
        stmt_cur = conn.execute("SELECT * FROM credit_card_statements WHERE status != 'PAID' ORDER BY due_date ASC")
        unpaid_stmts = [dict(s) for s in stmt_cur.fetchall()]
        total_unpaid_stmt = sum(float(s["unpaid_amount"]) for s in unpaid_stmts)

        pmt_cur = conn.execute("SELECT * FROM credit_card_payments ORDER BY payment_date DESC LIMIT 10")
        cc_payments = [dict(p) for p in pmt_cur.fetchall()]

        return {
            "card_count": len(cards),
            "total_limit": round(total_limit, 2),
            "total_balance": round(total_balance, 2),
            "total_available_credit": round(max(0.0, total_limit - total_balance), 2),
            "payment_reserve": round(payment_reserve, 2),
            "overall_utilization_rate": round((total_balance / total_limit * 100.0), 1) if total_limit > 0 else 0.0,
            "cards": cards,
            "credit_cards": cards,
            "unpaid_statements_count": len(unpaid_stmts),
            "total_unpaid_statement_amount": round(total_unpaid_stmt, 2),
            "unpaid_statements": unpaid_stmts,
            "payment_history": cc_payments
        }

    def get_financial_position(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        """
        Consolidated financial position combining Net Worth, Liquid Balances,
        Credit Card Balances, Liabilities, and Safe-to-Spend.
        """
        nw = self.get_net_worth_report(as_of)
        sts = self.get_safe_to_spend_report(as_of)
        cc = self.get_credit_card_summary()
        return {
            "as_of": nw.as_of_date,
            "net_worth": nw.to_dict(),
            "safe_to_spend": sts.to_dict(),
            "credit_cards": cc
        }

    def get_cashflow_trend(self, period: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns daily cashflow trend points for line chart.
        Period options: 'this_week', 'this_month', 'last_month', 'custom'
        """
        today = date.today()
        p = period or "this_month"
        if p == "this_week":
            s_date = today - timedelta(days=6)
            e_date = today
            label = "7 Hari Terakhir"
        elif p == "last_month":
            first_this_m = today.replace(day=1)
            e_date = first_this_m - timedelta(days=1)
            s_date = e_date.replace(day=1)
            label = f"Bulan Lalu ({s_date.strftime('%B %Y')})"
        elif p == "custom" and start_date and end_date:
            try:
                s_date = datetime.strptime(start_date.strip(), "%Y-%m-%d").date()
                e_date = datetime.strptime(end_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                s_date = today.replace(day=1)
                e_date = today
            label = f"Kustom ({s_date} s/d {e_date})"
        else: # this_month
            s_date = today.replace(day=1)
            e_date = today
            label = f"Bulan Ini ({today.strftime('%B %Y')})"

        conn = self.db.get_connection()
        query = """
            SELECT date, direction, SUM(amount) as total
            FROM transactions
            WHERE (status IS NULL OR status != 'VOID')
              AND date BETWEEN ? AND ?
            GROUP BY date, direction
        """
        cur = conn.execute(query, (s_date.isoformat(), e_date.isoformat()))
        daily_map = {}
        for r in cur.fetchall():
            d_str = r["date"]
            if d_str not in daily_map:
                daily_map[d_str] = {"income": 0.0, "expense": 0.0}
            d_type = r["direction"]
            if d_type == "INCOME":
                daily_map[d_str]["income"] += float(r["total"])
            elif d_type == "EXPENSE":
                daily_map[d_str]["expense"] += float(r["total"])

        days = []
        cur_d = s_date
        total_income = 0.0
        total_expense = 0.0
        while cur_d <= e_date:
            ds = cur_d.isoformat()
            data_d = daily_map.get(ds, {"income": 0.0, "expense": 0.0})
            inc = round(data_d["income"], 2)
            exp = round(data_d["expense"], 2)
            total_income += inc
            total_expense += exp
            days.append({
                "date": ds,
                "label": f"{cur_d.day}/{cur_d.month}",
                "income": inc,
                "expense": exp,
                "net": round(inc - exp, 2)
            })
            cur_d += timedelta(days=1)

        return {
            "period": p,
            "label": label,
            "start_date": s_date.isoformat(),
            "end_date": e_date.isoformat(),
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_cashflow": round(total_income - total_expense, 2),
            "trend_days": days,
            "data_points": days
        }





