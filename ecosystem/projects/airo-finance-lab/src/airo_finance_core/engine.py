import uuid
import hashlib
import secrets
from datetime import datetime, date, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple
from .db import DatabaseManager
from .models import (
    Account, Category, Transaction, Budget, AuditLog, FixedObligation, FinanceConfig,
    OwnerSession, Asset, Liability,
    Subcategory, CategoryAlias, TransactionMetadata, CorrectionEvent,
    ReviewQueueItem, CreditCard, CreditCardStatement, CreditCardPayment,
    LiabilityPayment, AssetValuation
)

class FinanceCoreEngine:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def _generate_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

    def _account_from_row(self, row) -> Account:
        keys = row.keys()
        return Account(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            balance=float(row["balance"]),
            is_active=row["is_active"] if "is_active" in keys else 1,
            created_at=row["created_at"],
            provider=row["provider"] if "provider" in keys else None,
            account_class=row["account_class"] if "account_class" in keys else "LIQUID",
            dashboard_group=row["dashboard_group"] if "dashboard_group" in keys else "CASH",
            parent_account_id=row["parent_account_id"] if "parent_account_id" in keys else None,
            aliases=row["aliases"] if "aliases" in keys else ""
        )

    def _category_from_row(self, row) -> Category:
        keys = row.keys()
        return Category(
            id=row["id"],
            name=row["name"],
            is_active=row["is_active"] if "is_active" in keys else 1,
            keywords=row["keywords"] if "keywords" in keys else "",
            created_at=row["created_at"],
            dashboard_group=row["dashboard_group"] if "dashboard_group" in keys else "GENERAL",
            domain=row["domain"] if "domain" in keys else "PERSONAL",
            event_type=row["event_type"] if "event_type" in keys else "REGULAR"
        )

    def _transaction_from_row(self, row) -> Transaction:
        keys = row.keys()
        return Transaction(
            id=row["id"],
            date=row["date"],
            account_id=row["account_id"],
            category_id=row["category_id"],
            amount=float(row["amount"]),
            direction=row["direction"],
            note=row["note"],
            source=row["source"],
            created_at=row["created_at"],
            subcategory_id=row["subcategory_id"] if "subcategory_id" in keys else None,
            status=row["status"] if "status" in keys and row["status"] else "ACTIVE",
            voided_at=row["voided_at"] if "voided_at" in keys else None,
            void_reason=row["void_reason"] if "void_reason" in keys else None,
            updated_at=row["updated_at"] if "updated_at" in keys else None
        )

    def create_account(
        self,
        name: str,
        account_type: str,
        initial_balance: float = 0.0,
        provider: Optional[str] = None,
        account_class: str = "LIQUID",
        dashboard_group: str = "CASH",
        parent_account_id: Optional[str] = None,
        aliases: str = ""
    ) -> Account:
        conn = self.db.get_connection()
        account_id = self._generate_id("acc")
        now_str = datetime.now(timezone.utc).isoformat()
        
        with conn:
            conn.execute(
                """INSERT INTO accounts 
                   (id, name, type, balance, is_active, created_at, provider, account_class, dashboard_group, parent_account_id, aliases) 
                   VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)""",
                (account_id, name, account_type.upper(), float(initial_balance), now_str,
                 provider, account_class, dashboard_group, parent_account_id, aliases)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "accounts", account_id, "CREATE", now_str)
            )
            
        return Account(
            id=account_id,
            name=name,
            type=account_type.upper(),
            balance=float(initial_balance),
            is_active=1,
            created_at=now_str,
            provider=provider,
            account_class=account_class,
            dashboard_group=dashboard_group,
            parent_account_id=parent_account_id,
            aliases=aliases
        )

    def update_account(
        self,
        account_id: str,
        name: Optional[str] = None,
        account_type: Optional[str] = None,
        is_active: Optional[int] = None,
        provider: Optional[str] = None,
        account_class: Optional[str] = None,
        dashboard_group: Optional[str] = None,
        parent_account_id: Optional[str] = None,
        aliases: Optional[str] = None
    ) -> Optional[Account]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cur.fetchone()
        if not row:
            return None

        keys = row.keys()
        new_name = name.strip() if name is not None else row["name"]
        if not new_name:
            raise ValueError("Account name cannot be empty")
        new_type = account_type.upper().strip() if account_type is not None else row["type"]
        new_active = int(is_active) if is_active is not None else (row["is_active"] if "is_active" in keys else 1)
        new_provider = provider if provider is not None else (row["provider"] if "provider" in keys else None)
        new_class = account_class if account_class is not None else (row["account_class"] if "account_class" in keys else "LIQUID")
        new_group = dashboard_group if dashboard_group is not None else (row["dashboard_group"] if "dashboard_group" in keys else "CASH")
        new_parent = parent_account_id if parent_account_id is not None else (row["parent_account_id"] if "parent_account_id" in keys else None)
        new_aliases = aliases if aliases is not None else (row["aliases"] if "aliases" in keys else "")

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                """UPDATE accounts 
                   SET name = ?, type = ?, is_active = ?, provider = ?, account_class = ?, dashboard_group = ?, parent_account_id = ?, aliases = ? 
                   WHERE id = ?""",
                (new_name, new_type, new_active, new_provider, new_class, new_group, new_parent, new_aliases, account_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "accounts", account_id, "UPDATE", now_str)
            )

        return Account(
            id=account_id,
            name=new_name,
            type=new_type,
            balance=float(row["balance"]),
            is_active=new_active,
            created_at=row["created_at"],
            provider=new_provider,
            account_class=new_class,
            dashboard_group=new_group,
            parent_account_id=new_parent,
            aliases=new_aliases
        )

    def list_accounts(self, active_only: bool = False) -> List[Account]:
        conn = self.db.get_connection()
        query = "SELECT * FROM accounts"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name ASC"
        cur = conn.execute(query)
        return [self._account_from_row(r) for r in cur.fetchall()]

    def create_category(
        self,
        name: str,
        keywords: str = "",
        dashboard_group: str = "GENERAL",
        domain: str = "PERSONAL",
        event_type: str = "REGULAR"
    ) -> Category:
        conn = self.db.get_connection()
        cat_id = self._generate_id("cat")
        now_str = datetime.now(timezone.utc).isoformat()
        kw_str = str(keywords).strip()
        
        with conn:
            conn.execute(
                """INSERT INTO categories 
                   (id, name, is_active, keywords, created_at, dashboard_group, domain, event_type) 
                   VALUES (?, ?, 1, ?, ?, ?, ?, ?)""",
                (cat_id, name, kw_str, now_str, dashboard_group, domain, event_type)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "categories", cat_id, "CREATE", now_str)
            )
            
        return Category(
            id=cat_id,
            name=name,
            is_active=1,
            keywords=kw_str,
            created_at=now_str,
            dashboard_group=dashboard_group,
            domain=domain,
            event_type=event_type
        )

    def update_category(
        self,
        category_id: str,
        name: Optional[str] = None,
        keywords: Optional[str] = None,
        is_active: Optional[int] = None,
        dashboard_group: Optional[str] = None,
        domain: Optional[str] = None,
        event_type: Optional[str] = None
    ) -> Optional[Category]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cur.fetchone()
        if not row:
            return None

        keys = row.keys()
        new_name = name.strip() if name is not None else row["name"]
        if not new_name:
            raise ValueError("Category name cannot be empty")
        new_kw = str(keywords).strip() if keywords is not None else (row["keywords"] if "keywords" in keys else "")
        new_active = int(is_active) if is_active is not None else (row["is_active"] if "is_active" in keys else 1)
        new_group = dashboard_group if dashboard_group is not None else (row["dashboard_group"] if "dashboard_group" in keys else "GENERAL")
        new_domain = domain if domain is not None else (row["domain"] if "domain" in keys else "PERSONAL")
        new_event = event_type if event_type is not None else (row["event_type"] if "event_type" in keys else "REGULAR")

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                """UPDATE categories 
                   SET name = ?, keywords = ?, is_active = ?, dashboard_group = ?, domain = ?, event_type = ? 
                   WHERE id = ?""",
                (new_name, new_kw, new_active, new_group, new_domain, new_event, category_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "categories", category_id, "UPDATE", now_str)
            )

        return Category(
            id=category_id,
            name=new_name,
            is_active=new_active,
            keywords=new_kw,
            created_at=row["created_at"],
            dashboard_group=new_group,
            domain=new_domain,
            event_type=new_event
        )

    def list_categories(self, active_only: bool = False) -> List[Category]:
        conn = self.db.get_connection()
        query = "SELECT * FROM categories"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name ASC"
        cur = conn.execute(query)
        return [self._category_from_row(r) for r in cur.fetchall()]

    def get_account(self, account_id: str) -> Optional[Account]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._account_from_row(row)

    def get_account_by_name(self, name: str) -> Optional[Account]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE LOWER(name) = LOWER(?)", (name.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return self._account_from_row(row)

    def get_category(self, category_id: str) -> Optional[Category]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._category_from_row(row)

    def get_category_by_name(self, name: str) -> Optional[Category]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM categories WHERE LOWER(name) = LOWER(?)", (name.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return self._category_from_row(row)



    def create_transaction(
        self,
        account_id: str,
        amount: float,
        direction: str,
        category_id: Optional[str] = None,
        note: Optional[str] = None,
        source: str = "MANUAL",
        tx_date: Optional[str] = None,
        subcategory_id: Optional[str] = None
    ) -> Transaction:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
            
        direction = direction.upper()
        if direction not in ("EXPENSE", "INCOME", "TRANSFER", "ASSET_PURCHASE"):
            raise ValueError(f"Invalid direction: {direction}")
            
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        acc_row = cur.fetchone()
        if not acc_row:
            raise ValueError(f"Account not found: {account_id}")
            
        if category_id:
            cur = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            if not cur.fetchone():
                raise ValueError(f"Category not found: {category_id}")

        if subcategory_id:
            sub_cur = conn.execute("SELECT * FROM subcategories WHERE id = ?", (subcategory_id,))
            sub_row = sub_cur.fetchone()
            if not sub_row:
                raise ValueError(f"Subcategory not found: {subcategory_id}")
            if category_id and sub_row["category_id"] != category_id:
                raise ValueError(f"Subcategory {subcategory_id} does not belong to category {category_id}")
                
        tx_id = self._generate_id("tx")
        if not tx_date:
            tx_date = date.today().isoformat()
        now_str = datetime.now(timezone.utc).isoformat()
        
        with conn:
            # 1. Update account balance
            if direction == "EXPENSE":
                new_balance = acc_row["balance"] - amount
            elif direction == "INCOME":
                new_balance = acc_row["balance"] + amount
            elif direction == "ASSET_PURCHASE":
                new_balance = acc_row["balance"] - amount
            else: # TRANSFER
                new_balance = acc_row["balance"] - amount
                
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
            
            # 2. Insert transaction
            conn.execute(
                "INSERT INTO transactions "
                "(id, date, account_id, category_id, subcategory_id, amount, direction, note, source, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)",
                (tx_id, tx_date, account_id, category_id, subcategory_id, amount, direction, note, source, now_str, now_str)
            )

            if subcategory_id:
                self.record_transaction_metadata(tx_id, subcategory_id=subcategory_id)
            
            # 3. Create audit log
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "transactions", tx_id, "CREATE", now_str)
            )
            
        return Transaction(
            id=tx_id,
            date=tx_date,
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            direction=direction,
            note=note,
            source=source,
            created_at=now_str,
            subcategory_id=subcategory_id,
            status='ACTIVE',
            voided_at=None,
            void_reason=None,
            updated_at=now_str
        )

    def transfer_funds(
        self,
        source_account_id: str,
        destination_account_id: str,
        amount: float,
        note: Optional[str] = None,
        source: str = "MANUAL",
        tx_date: Optional[str] = None
    ) -> Tuple[Transaction, Transaction]:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if source_account_id == destination_account_id:
            raise ValueError("Source and destination accounts must be different")

        conn = self.db.get_connection()
        
        # Verify source account exists
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (source_account_id,))
        src_row = cur.fetchone()
        if not src_row:
            raise ValueError(f"Source account not found: {source_account_id}")

        # Verify destination account exists
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (destination_account_id,))
        dst_row = cur.fetchone()
        if not dst_row:
            raise ValueError(f"Destination account not found: {destination_account_id}")

        tx_out_id = self._generate_id("tx")
        tx_in_id = self._generate_id("tx")
        if not tx_date:
            tx_date = date.today().isoformat()
        now_str = datetime.now(timezone.utc).isoformat()

        user_note = f" ({note})" if note else ""
        out_note = f"Transfer ke {dst_row['name']}{user_note}"
        in_note = f"Transfer dari {src_row['name']}{user_note}"

        with conn:
            # 1. Update source account balance (deduct)
            new_src_balance = src_row["balance"] - amount
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_src_balance, source_account_id))

            # 2. Update destination account balance (add)
            new_dst_balance = dst_row["balance"] + amount
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_dst_balance, destination_account_id))

            # 3. Insert Outflow Transaction
            conn.execute(
                "INSERT INTO transactions "
                "(id, date, account_id, category_id, amount, direction, note, source, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (tx_out_id, tx_date, source_account_id, None, amount, "TRANSFER", out_note, source, now_str)
            )

            # 4. Insert Inflow Transaction
            conn.execute(
                "INSERT INTO transactions "
                "(id, date, account_id, category_id, amount, direction, note, source, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (tx_in_id, tx_date, destination_account_id, None, amount, "TRANSFER", in_note, source, now_str)
            )

            # 5. Create Audit Logs
            aud_out = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (aud_out, "transactions", tx_out_id, "TRANSFER_OUT", now_str)
            )
            aud_in = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (aud_in, "transactions", tx_in_id, "TRANSFER_IN", now_str)
            )

        tx_out = Transaction(
            id=tx_out_id,
            date=tx_date,
            account_id=source_account_id,
            category_id=None,
            amount=amount,
            direction="TRANSFER",
            note=out_note,
            source=source,
            created_at=now_str
        )
        tx_in = Transaction(
            id=tx_in_id,
            date=tx_date,
            account_id=destination_account_id,
            category_id=None,
            amount=amount,
            direction="TRANSFER",
            note=in_note,
            source=source,
            created_at=now_str
        )
        return tx_out, tx_in

    def calculate_running_balances(self, account_id: Optional[str] = None) -> Dict[str, float]:
        """
        Calculates chronological running balance per transaction.
        Handles:
        - EXPENSE: Decreases account balance
        - INCOME: Increases account balance
        - TRANSFER: Decreases source account, increases destination account
        - CREDIT_CARD_PURCHASE: Increases credit card liability (does NOT decrease cash account)
        - CREDIT_CARD_PAYMENT: Decreases payment cash account, decreases credit card liability
        Returns a mapping of transaction_id -> running_balance (the balance of transaction.account_id after tx).
        """
        conn = self.db.get_connection()
        query = """
            SELECT t.*, a.type as account_type, a.account_class, a.name as account_name
            FROM transactions t
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE t.status IS NULL OR t.status != 'VOID'
            ORDER BY t.date ASC, t.created_at ASC, t.id ASC
        """
        rows = conn.execute(query).fetchall()

        # Track simulated balance per account starting from 0.0 or replay
        # To match authoritative account.balance, initial balance is (current_balance - sum_of_deltas)
        # First calculate total delta per account:
        account_deltas: Dict[str, float] = {}
        for r in rows:
            acc_id = r["account_id"]
            direction = r["direction"]
            amt = float(r["amount"])
            note = (r["note"] or "").lower()
            src = (r["source"] or "").upper()
            acc_type = (r["account_type"] or "").upper()
            acc_class = (r["account_class"] or "").upper()
            is_cc = acc_type == "CREDIT_CARD" or acc_class == "LIABILITY"

            # Determine signed effect on account_id
            if direction == "INCOME":
                delta = amt
            elif direction == "EXPENSE":
                delta = -amt
            elif direction == "TRANSFER":
                if "transfer dari" in note:
                    delta = amt
                else: # transfer ke
                    delta = -amt
            elif direction == "CREDIT_CARD_PURCHASE":
                delta = amt if is_cc else -amt
            elif direction == "CREDIT_CARD_PAYMENT":
                delta = -amt
            else:
                delta = -amt

            account_deltas[acc_id] = account_deltas.get(acc_id, 0.0) + delta

        # Query current balances from accounts table
        acc_rows = conn.execute("SELECT id, balance FROM accounts").fetchall()
        cur_balances = {ar["id"]: float(ar["balance"]) for ar in acc_rows}

        # Baseline balance before any transactions were applied:
        sim_balances: Dict[str, float] = {}
        for aid, cur_bal in cur_balances.items():
            sim_balances[aid] = cur_bal - account_deltas.get(aid, 0.0)

        running_balances: Dict[str, float] = {}
        for r in rows:
            tx_id = r["id"]
            acc_id = r["account_id"]
            direction = r["direction"]
            amt = float(r["amount"])
            note = (r["note"] or "").lower()
            src = (r["source"] or "").upper()
            acc_type = (r["account_type"] or "").upper()
            acc_class = (r["account_class"] or "").upper()
            is_cc = acc_type == "CREDIT_CARD" or acc_class == "LIABILITY"

            if direction == "INCOME":
                delta = amt
            elif direction == "EXPENSE":
                delta = -amt
            elif direction == "TRANSFER":
                if "transfer dari" in note:
                    delta = amt
                else:
                    delta = -amt
            elif direction == "CREDIT_CARD_PURCHASE":
                delta = amt if is_cc else -amt
            elif direction == "CREDIT_CARD_PAYMENT":
                delta = -amt
            else:
                delta = -amt

            new_bal = sim_balances.get(acc_id, 0.0) + delta
            sim_balances[acc_id] = new_bal
            running_balances[tx_id] = round(new_bal, 2)

        if account_id:
            return {
                r["id"]: running_balances[r["id"]]
                for r in rows
                if r["account_id"] == account_id and r["id"] in running_balances
            }
        return running_balances

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        row = cur.fetchone()
        if not row:
            return None
        tx = self._transaction_from_row(row)
        rb_map = self.calculate_running_balances()
        tx.running_balance = rb_map.get(tx.id)
        return tx

    def list_transactions(self, limit: int = 50, account_id: Optional[str] = None) -> List[Transaction]:
        conn = self.db.get_connection()
        query = "SELECT * FROM transactions"
        params = []
        if account_id:
            query += " WHERE account_id = ?"
            params.append(account_id)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        cur = conn.execute(query, params)
        txs = [self._transaction_from_row(r) for r in cur.fetchall()]
        rb_map = self.calculate_running_balances()
        for tx in txs:
            tx.running_balance = rb_map.get(tx.id)
        return txs

    def get_audit_logs(self, limit: int = 50) -> List[AuditLog]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT ?", (limit,))
        return [
            AuditLog(
                id=r["id"],
                entity=r["entity"],
                entity_id=r["entity_id"],
                action=r["action"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    # ----------------------------------------------------
    # Fixed Obligations CRUD
    # ----------------------------------------------------
    def create_fixed_obligation(
        self,
        name: str,
        amount: float,
        due_day: int,
        category_id: Optional[str] = None
    ) -> FixedObligation:
        name = name.strip()
        if not name:
            raise ValueError("Obligation name cannot be empty")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Obligation amount must be greater than 0")
        due_day = int(due_day)
        if not (1 <= due_day <= 31):
            raise ValueError("Due day must be between 1 and 31")

        conn = self.db.get_connection()
        if category_id:
            cur = conn.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
            if not cur.fetchone():
                raise ValueError(f"Category not found: {category_id}")

        obl_id = self._generate_id("obl")
        now_str = datetime.now(timezone.utc).isoformat()

        with conn:
            conn.execute(
                "INSERT INTO fixed_obligations (id, name, amount, due_day, category_id, is_active, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
                (obl_id, name, amount, due_day, category_id, now_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "fixed_obligations", obl_id, "CREATE", now_str)
            )

        return FixedObligation(
            id=obl_id,
            name=name,
            amount=amount,
            due_day=due_day,
            category_id=category_id,
            is_active=1,
            created_at=now_str,
            updated_at=now_str
        )

    def update_fixed_obligation(
        self,
        obligation_id: str,
        name: Optional[str] = None,
        amount: Optional[float] = None,
        due_day: Optional[int] = None,
        category_id: Optional[str] = None,
        is_active: Optional[int] = None
    ) -> Optional[FixedObligation]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM fixed_obligations WHERE id = ?", (obligation_id,))
        row = cur.fetchone()
        if not row:
            return None

        new_name = name.strip() if name is not None else row["name"]
        if not new_name:
            raise ValueError("Obligation name cannot be empty")

        new_amount = float(amount) if amount is not None else float(row["amount"])
        if new_amount <= 0:
            raise ValueError("Obligation amount must be greater than 0")

        new_due_day = int(due_day) if due_day is not None else int(row["due_day"])
        if not (1 <= new_due_day <= 31):
            raise ValueError("Due day must be between 1 and 31")

        new_cat = category_id if category_id is not None else row["category_id"]
        if new_cat:
            cat_cur = conn.execute("SELECT id FROM categories WHERE id = ?", (new_cat,))
            if not cat_cur.fetchone():
                raise ValueError(f"Category not found: {new_cat}")

        new_active = int(is_active) if is_active is not None else int(row["is_active"])
        if new_active not in (0, 1):
            raise ValueError("is_active must be 0 or 1")

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "UPDATE fixed_obligations SET name = ?, amount = ?, due_day = ?, category_id = ?, is_active = ?, updated_at = ? WHERE id = ?",
                (new_name, new_amount, new_due_day, new_cat, new_active, now_str, obligation_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "fixed_obligations", obligation_id, "UPDATE", now_str)
            )

        return FixedObligation(
            id=obligation_id,
            name=new_name,
            amount=new_amount,
            due_day=new_due_day,
            category_id=new_cat,
            is_active=new_active,
            created_at=row["created_at"],
            updated_at=now_str
        )

    def get_fixed_obligation(self, obligation_id: str) -> Optional[FixedObligation]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM fixed_obligations WHERE id = ?", (obligation_id,))
        row = cur.fetchone()
        if not row:
            return None
        return FixedObligation(
            id=row["id"],
            name=row["name"],
            amount=float(row["amount"]),
            due_day=int(row["due_day"]),
            category_id=row["category_id"],
            is_active=int(row["is_active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def list_fixed_obligations(self, active_only: bool = False) -> List[FixedObligation]:
        conn = self.db.get_connection()
        query = "SELECT * FROM fixed_obligations"
        params = []
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY due_day ASC, name ASC"
        cur = conn.execute(query, params)
        return [
            FixedObligation(
                id=r["id"],
                name=r["name"],
                amount=float(r["amount"]),
                due_day=int(r["due_day"]),
                category_id=r["category_id"],
                is_active=int(r["is_active"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in cur.fetchall()
        ]

    def delete_fixed_obligation(self, obligation_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT id FROM fixed_obligations WHERE id = ?", (obligation_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute("DELETE FROM fixed_obligations WHERE id = ?", (obligation_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "fixed_obligations", obligation_id, "DELETE", now_str)
            )
        return True

    # ----------------------------------------------------
    # Finance Configuration Management
    # ----------------------------------------------------
    def get_config(self, key: str, default: Optional[str] = None) -> Optional[str]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT value FROM finance_config WHERE key = ?", (key,))
        row = cur.fetchone()
        if row:
            return str(row["value"])
        return default

    def get_all_config(self) -> Dict[str, str]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT key, value FROM finance_config ORDER BY key ASC")
        return {r["key"]: str(r["value"]) for r in cur.fetchall()}

    def set_config(self, key: str, value: str) -> FinanceConfig:
        key = key.strip()
        val_str = str(value).strip()
        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "INSERT INTO finance_config (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
                (key, val_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "finance_config", key, "UPDATE", now_str)
            )
        return FinanceConfig(key=key, value=val_str, updated_at=now_str)

    # ----------------------------------------------------
    # Package 0: Owner Access Session Layer
    # ----------------------------------------------------
    def create_owner_session(self, device_name: str = "Web Browser", expiry_days: int = 30, expires_in_days: Optional[int] = None) -> Tuple[OwnerSession, str]:
        if expires_in_days is not None:
            expiry_days = expires_in_days
        device_name = (device_name or "Web Browser").strip()
        session_id = self._generate_id("sess")
        raw_token = secrets.token_hex(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()
        expires_at = (now + timedelta(days=expiry_days)).isoformat()
        
        conn = self.db.get_connection()
        with conn:
            conn.execute(
                "INSERT INTO owner_sessions (id, token_hash, device_name, created_at, expires_at, last_used_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (session_id, token_hash, device_name, now_str, expires_at, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "owner_sessions", session_id, "LOGIN", now_str)
            )
            
        session = OwnerSession(
            id=session_id,
            token_hash=token_hash,
            device_name=device_name,
            created_at=now_str,
            expires_at=expires_at,
            last_used_at=now_str,
            revoked_at=None
        )
        return session, raw_token

    def verify_owner_session(self, raw_token: str) -> Optional[OwnerSession]:
        if not raw_token:
            return None
        token_hash = hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()
        conn = self.db.get_connection()
        cur = conn.execute(
            "SELECT * FROM owner_sessions WHERE token_hash = ? AND revoked_at IS NULL",
            (token_hash,)
        )
        row = cur.fetchone()
        if not row:
            return None
            
        now_utc = datetime.now(timezone.utc)
        expires_at = datetime.fromisoformat(row["expires_at"])
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if now_utc > expires_at:
            return None
            
        now_str = now_utc.isoformat()
        with conn:
            conn.execute("UPDATE owner_sessions SET last_used_at = ? WHERE id = ?", (now_str, row["id"]))
            
        return OwnerSession(
            id=row["id"],
            token_hash=row["token_hash"],
            device_name=row["device_name"],
            created_at=row["created_at"],
            expires_at=row["expires_at"],
            last_used_at=now_str,
            revoked_at=None
        )

    def revoke_owner_session(self, raw_token: str) -> bool:
        if not raw_token:
            return False
        token_hash = hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()
        conn = self.db.get_connection()
        cur = conn.execute("SELECT id FROM owner_sessions WHERE token_hash = ? AND revoked_at IS NULL", (token_hash,))
        row = cur.fetchone()
        if not row:
            return False
            
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute("UPDATE owner_sessions SET revoked_at = ? WHERE id = ?", (now_str, row["id"]))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "owner_sessions", row["id"], "LOGOUT", now_str)
            )
        return True

    def revoke_all_owner_sessions(self) -> int:
        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            cur = conn.execute("SELECT count(*) as c FROM owner_sessions WHERE revoked_at IS NULL")
            count = cur.fetchone()["c"]
            conn.execute("UPDATE owner_sessions SET revoked_at = ? WHERE revoked_at IS NULL", (now_str,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "owner_sessions", "ALL", "LOGOUT_ALL", now_str)
            )
        return count

    def list_owner_sessions(self, active_only: bool = True) -> List[OwnerSession]:
        conn = self.db.get_connection()
        query = "SELECT * FROM owner_sessions"
        if active_only:
            now_str = datetime.now(timezone.utc).isoformat()
            query += f" WHERE revoked_at IS NULL AND expires_at > '{now_str}'"
        query += " ORDER BY created_at DESC"
        cur = conn.execute(query)
        return [
            OwnerSession(
                id=r["id"],
                token_hash=r["token_hash"],
                device_name=r["device_name"],
                created_at=r["created_at"],
                expires_at=r["expires_at"],
                last_used_at=r["last_used_at"],
                revoked_at=r["revoked_at"]
            )
            for r in cur.fetchall()
        ]

    # ----------------------------------------------------
    # Package A: Asset Registry CRUD
    # ----------------------------------------------------
    def create_asset(
        self,
        name: str,
        asset_type: str,
        current_value: float,
        notes: Optional[str] = None,
        asset_class: str = "OTHER",
        weight_grams: float = 0.0,
        purchase_cost: float = 0.0,
        average_cost_per_gram: float = 0.0,
        current_unit_price: float = 0.0
    ) -> Asset:
        name = name.strip()
        if not name:
            raise ValueError("Asset name cannot be empty")
        current_value = float(current_value)
        if current_value < 0:
            raise ValueError("Asset value cannot be negative")
        asset_type = asset_type.upper().strip()
        if not asset_type:
            asset_type = "OTHER"

        conn = self.db.get_connection()
        asset_id = self._generate_id("ast")
        now_str = datetime.now(timezone.utc).isoformat()

        # Check if extended columns exist
        cur = conn.execute("PRAGMA table_info(assets)")
        cols = [r["name"] for r in cur.fetchall()]
        has_extended = "asset_class" in cols

        avg_cost = average_cost_per_gram
        if avg_cost == 0.0 and weight_grams > 0 and purchase_cost > 0:
            avg_cost = round(purchase_cost / weight_grams, 2)

        with conn:
            if has_extended:
                conn.execute(
                    "INSERT INTO assets (id, name, type, current_value, notes, is_active, created_at, updated_at, "
                    "asset_class, weight_grams, purchase_cost, average_cost_per_gram, current_unit_price) "
                    "VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)",
                    (asset_id, name, asset_type, current_value, notes, now_str, now_str,
                     asset_class, weight_grams, purchase_cost, avg_cost, current_unit_price)
                )
            else:
                conn.execute(
                    "INSERT INTO assets (id, name, type, current_value, notes, is_active, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
                    (asset_id, name, asset_type, current_value, notes, now_str, now_str)
                )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "assets", asset_id, "CREATE", now_str)
            )

        return Asset(
            id=asset_id,
            name=name,
            type=asset_type,
            current_value=current_value,
            notes=notes,
            is_active=1,
            created_at=now_str,
            updated_at=now_str,
            asset_class=asset_class,
            weight_grams=weight_grams,
            purchase_cost=purchase_cost,
            average_cost_per_gram=avg_cost,
            current_unit_price=current_unit_price
        )

    def update_asset(
        self,
        asset_id: str,
        name: Optional[str] = None,
        asset_type: Optional[str] = None,
        current_value: Optional[float] = None,
        notes: Optional[str] = None,
        is_active: Optional[int] = None
    ) -> Optional[Asset]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
        row = cur.fetchone()
        if not row:
            return None

        new_name = name.strip() if name is not None else row["name"]
        if not new_name:
            raise ValueError("Asset name cannot be empty")
        new_type = asset_type.upper().strip() if asset_type is not None else row["type"]
        new_val = float(current_value) if current_value is not None else float(row["current_value"])
        if new_val < 0:
            raise ValueError("Asset value cannot be negative")
        new_notes = notes if notes is not None else row["notes"]
        new_active = int(is_active) if is_active is not None else int(row["is_active"])

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "UPDATE assets SET name = ?, type = ?, current_value = ?, notes = ?, is_active = ?, updated_at = ? WHERE id = ?",
                (new_name, new_type, new_val, new_notes, new_active, now_str, asset_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "assets", asset_id, "UPDATE", now_str)
            )

        return Asset(
            id=asset_id,
            name=new_name,
            type=new_type,
            current_value=new_val,
            notes=new_notes,
            is_active=new_active,
            created_at=row["created_at"],
            updated_at=now_str
        )

    def _asset_from_row(self, row) -> Asset:
        keys = row.keys()
        return Asset(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            current_value=float(row["current_value"]),
            notes=row["notes"],
            is_active=int(row["is_active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            asset_class=row["asset_class"] if "asset_class" in keys and row["asset_class"] else "OTHER",
            weight_grams=float(row["weight_grams"]) if "weight_grams" in keys and row["weight_grams"] is not None else 0.0,
            purchase_cost=float(row["purchase_cost"]) if "purchase_cost" in keys and row["purchase_cost"] is not None else 0.0,
            average_cost_per_gram=float(row["average_cost_per_gram"]) if "average_cost_per_gram" in keys and row["average_cost_per_gram"] is not None else 0.0,
            current_unit_price=float(row["current_unit_price"]) if "current_unit_price" in keys and row["current_unit_price"] is not None else 0.0
        )

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._asset_from_row(row)

    def list_assets(self, active_only: bool = False) -> List[Asset]:
        conn = self.db.get_connection()
        query = "SELECT * FROM assets"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY current_value DESC, name ASC"
        cur = conn.execute(query)
        return [self._asset_from_row(r) for r in cur.fetchall()]

    def delete_asset(self, asset_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT id FROM assets WHERE id = ?", (asset_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "assets", asset_id, "DELETE", now_str)
            )
        return True

    # ----------------------------------------------------
    # Package A: Liability Registry CRUD
    # ----------------------------------------------------
    def create_liability(
        self,
        name: str,
        liability_type: str,
        original_amount: float,
        remaining_amount: float,
        monthly_payment: float,
        due_day: int,
        notes: Optional[str] = None
    ) -> Liability:
        name = name.strip()
        if not name:
            raise ValueError("Liability name cannot be empty")
        liability_type = liability_type.upper().strip()
        if not liability_type:
            liability_type = "OTHER"
        orig_val = float(original_amount)
        rem_val = float(remaining_amount)
        mon_val = float(monthly_payment)
        if orig_val < 0 or rem_val < 0 or mon_val < 0:
            raise ValueError("Liability amounts cannot be negative")
        due_day = int(due_day)
        if not (1 <= due_day <= 31):
            raise ValueError("Due day must be between 1 and 31")

        conn = self.db.get_connection()
        liab_id = self._generate_id("liab")
        now_str = datetime.now(timezone.utc).isoformat()

        with conn:
            conn.execute(
                "INSERT INTO liabilities (id, name, type, original_amount, remaining_amount, monthly_payment, due_day, notes, is_active, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
                (liab_id, name, liability_type, orig_val, rem_val, mon_val, due_day, notes, now_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "liabilities", liab_id, "CREATE", now_str)
            )

        return Liability(
            id=liab_id,
            name=name,
            type=liability_type,
            original_amount=orig_val,
            remaining_amount=rem_val,
            monthly_payment=mon_val,
            due_day=due_day,
            notes=notes,
            is_active=1,
            created_at=now_str,
            updated_at=now_str
        )

    def update_liability(
        self,
        liability_id: str,
        name: Optional[str] = None,
        liability_type: Optional[str] = None,
        original_amount: Optional[float] = None,
        remaining_amount: Optional[float] = None,
        monthly_payment: Optional[float] = None,
        due_day: Optional[int] = None,
        notes: Optional[str] = None,
        is_active: Optional[int] = None
    ) -> Optional[Liability]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM liabilities WHERE id = ?", (liability_id,))
        row = cur.fetchone()
        if not row:
            return None

        new_name = name.strip() if name is not None else row["name"]
        if not new_name:
            raise ValueError("Liability name cannot be empty")
        new_type = liability_type.upper().strip() if liability_type is not None else row["type"]
        new_orig = float(original_amount) if original_amount is not None else float(row["original_amount"])
        new_rem = float(remaining_amount) if remaining_amount is not None else float(row["remaining_amount"])
        new_mon = float(monthly_payment) if monthly_payment is not None else float(row["monthly_payment"])
        if new_orig < 0 or new_rem < 0 or new_mon < 0:
            raise ValueError("Liability amounts cannot be negative")
        new_due = int(due_day) if due_day is not None else int(row["due_day"])
        if not (1 <= new_due <= 31):
            raise ValueError("Due day must be between 1 and 31")
        new_notes = notes if notes is not None else row["notes"]
        new_active = int(is_active) if is_active is not None else int(row["is_active"])

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "UPDATE liabilities SET name = ?, type = ?, original_amount = ?, remaining_amount = ?, monthly_payment = ?, due_day = ?, notes = ?, is_active = ?, updated_at = ? WHERE id = ?",
                (new_name, new_type, new_orig, new_rem, new_mon, new_due, new_notes, new_active, now_str, liability_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "liabilities", liability_id, "UPDATE", now_str)
            )

        return Liability(
            id=liability_id,
            name=new_name,
            type=new_type,
            original_amount=new_orig,
            remaining_amount=new_rem,
            monthly_payment=new_mon,
            due_day=new_due,
            notes=new_notes,
            is_active=new_active,
            created_at=row["created_at"],
            updated_at=now_str
        )

    def get_liability(self, liability_id: str) -> Optional[Liability]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM liabilities WHERE id = ?", (liability_id,))
        row = cur.fetchone()
        if not row:
            return None
        return Liability(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            original_amount=float(row["original_amount"]),
            remaining_amount=float(row["remaining_amount"]),
            monthly_payment=float(row["monthly_payment"]),
            due_day=int(row["due_day"]),
            notes=row["notes"],
            is_active=int(row["is_active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def list_liabilities(self, active_only: bool = False) -> List[Liability]:
        conn = self.db.get_connection()
        query = "SELECT * FROM liabilities"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY remaining_amount DESC, name ASC"
        cur = conn.execute(query)
        return [
            Liability(
                id=r["id"],
                name=r["name"],
                type=r["type"],
                original_amount=float(r["original_amount"]),
                remaining_amount=float(r["remaining_amount"]),
                monthly_payment=float(r["monthly_payment"]),
                due_day=int(r["due_day"]),
                notes=r["notes"],
                is_active=int(r["is_active"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in cur.fetchall()
        ]

    def delete_liability(self, liability_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT id FROM liabilities WHERE id = ?", (liability_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute("DELETE FROM liabilities WHERE id = ?", (liability_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "liabilities", liability_id, "DELETE", now_str)
            )
        return True

    # ====================================================
    # Phase 3.1: Subcategories
    # ====================================================
    def create_subcategory(self, category_id: str, name: str, display_order: int = 0) -> Subcategory:
        conn = self.db.get_connection()
        subcat_id = self._generate_id("subcat")
        now_str = datetime.now(timezone.utc).isoformat()
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Subcategory name cannot be empty")
        with conn:
            conn.execute(
                "INSERT INTO subcategories (id, category_id, name, display_order, is_active, created_at) VALUES (?, ?, ?, ?, 1, ?)",
                (subcat_id, category_id, clean_name, display_order, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "subcategories", subcat_id, "CREATE", now_str)
            )
        return Subcategory(id=subcat_id, category_id=category_id, name=clean_name, display_order=display_order, is_active=1, created_at=now_str)

    def update_subcategory(
        self,
        subcategory_id: str,
        name: Optional[str] = None,
        display_order: Optional[int] = None,
        is_active: Optional[int] = None
    ) -> Optional[Subcategory]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM subcategories WHERE id = ?", (subcategory_id,))
        row = cur.fetchone()
        if not row:
            return None
        new_name = name.strip() if name is not None else row["name"]
        new_order = int(display_order) if display_order is not None else row["display_order"]
        new_active = int(is_active) if is_active is not None else row["is_active"]
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "UPDATE subcategories SET name = ?, display_order = ?, is_active = ? WHERE id = ?",
                (new_name, new_order, new_active, subcategory_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "subcategories", subcategory_id, "UPDATE", now_str)
            )
        return Subcategory(id=subcategory_id, category_id=row["category_id"], name=new_name, display_order=new_order, is_active=new_active, created_at=row["created_at"])

    def list_subcategories(self, category_id: Optional[str] = None, active_only: bool = False) -> List[Subcategory]:
        conn = self.db.get_connection()
        query = "SELECT * FROM subcategories WHERE 1=1"
        params = []
        if category_id:
            query += " AND category_id = ?"
            params.append(category_id)
        if active_only:
            query += " AND is_active = 1"
        query += " ORDER BY display_order ASC, name ASC"
        cur = conn.execute(query, params)
        return [
            Subcategory(
                id=r["id"],
                category_id=r["category_id"],
                name=r["name"],
                display_order=r["display_order"],
                is_active=r["is_active"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    def get_subcategory(self, subcategory_id: str) -> Optional[Subcategory]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM subcategories WHERE id = ?", (subcategory_id,))
        r = cur.fetchone()
        if not r:
            return None
        return Subcategory(
            id=r["id"],
            category_id=r["category_id"],
            name=r["name"],
            display_order=r["display_order"],
            is_active=r["is_active"],
            created_at=r["created_at"]
        )

    # ====================================================
    # Phase 3.1: Category Aliases
    # ====================================================
    def add_category_alias(
        self,
        keyword: str,
        subcategory_id: Optional[str] = None,
        category_id: Optional[str] = None,
        priority: int = 10
    ) -> CategoryAlias:
        conn = self.db.get_connection()
        alias_id = self._generate_id("alias")
        now_str = datetime.now(timezone.utc).isoformat()
        clean_kw = keyword.strip().lower()
        if not clean_kw:
            raise ValueError("Alias keyword cannot be empty")
        if not category_id and subcategory_id:
            subcat = self.get_subcategory(subcategory_id)
            if subcat:
                category_id = subcat.category_id

        with conn:
            conn.execute(
                "INSERT INTO category_aliases (id, subcategory_id, category_id, keyword, priority, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (alias_id, subcategory_id, category_id, clean_kw, priority, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "category_aliases", alias_id, "CREATE", now_str)
            )
        return CategoryAlias(id=alias_id, keyword=clean_kw, subcategory_id=subcategory_id, category_id=category_id, priority=priority, created_at=now_str)

    def delete_category_alias(self, alias_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT id FROM category_aliases WHERE id = ?", (alias_id,))
        if not cur.fetchone():
            return False
        with conn:
            conn.execute("DELETE FROM category_aliases WHERE id = ?", (alias_id,))
            audit_id = self._generate_id("aud")
            now_str = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "category_aliases", alias_id, "DELETE", now_str)
            )
        return True

    def list_category_aliases(self, category_id: Optional[str] = None, subcategory_id: Optional[str] = None) -> List[CategoryAlias]:
        conn = self.db.get_connection()
        query = "SELECT * FROM category_aliases WHERE 1=1"
        params = []
        if subcategory_id:
            query += " AND subcategory_id = ?"
            params.append(subcategory_id)
        elif category_id:
            query += " AND category_id = ?"
            params.append(category_id)
        query += " ORDER BY priority DESC, keyword ASC"
        cur = conn.execute(query, params)
        return [
            CategoryAlias(
                id=r["id"],
                keyword=r["keyword"],
                subcategory_id=r["subcategory_id"],
                category_id=r["category_id"],
                priority=r["priority"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    def find_category_by_keyword(self, text: str) -> Optional[Dict[str, Any]]:
        conn = self.db.get_connection()
        clean = (text or "").lower().strip()
        if not clean:
            return None
        cur = conn.execute(
            """SELECT a.*, c.name as cat_name, s.name as subcat_name 
               FROM category_aliases a
               LEFT JOIN categories c ON a.category_id = c.id
               LEFT JOIN subcategories s ON a.subcategory_id = s.id
               ORDER BY a.priority DESC, LENGTH(a.keyword) DESC"""
        )
        for r in cur.fetchall():
            kw = r["keyword"].lower()
            if kw == clean or kw in clean or clean in kw:
                return {
                    "category_id": r["category_id"],
                    "category_name": r["cat_name"],
                    "subcategory_id": r["subcategory_id"],
                    "subcategory_name": r["subcat_name"],
                    "matched_keyword": kw,
                    "confidence": 0.95 if kw == clean else 0.85
                }
        cats = self.list_categories(active_only=True)
        for cat in cats:
            kws = [k.strip().lower() for k in cat.keywords.split(",") if k.strip()]
            for kw in kws:
                if kw == clean or kw in clean:
                    return {
                        "category_id": cat.id,
                        "category_name": cat.name,
                        "subcategory_id": None,
                        "subcategory_name": None,
                        "matched_keyword": kw,
                        "confidence": 0.8
                    }
        return None

    # ====================================================
    # Phase 3.1: Transaction Metadata & Corrections
    # ====================================================
    def record_transaction_metadata(
        self,
        transaction_id: str,
        subcategory_id: Optional[str] = None,
        raw_input: Optional[str] = None,
        source_type: str = "MANUAL",
        confidence_score: float = 1.0
    ) -> TransactionMetadata:
        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                """INSERT OR REPLACE INTO transaction_metadata 
                   (transaction_id, subcategory_id, raw_input, source_type, confidence_score, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (transaction_id, subcategory_id, raw_input, source_type, float(confidence_score), now_str)
            )
        return TransactionMetadata(
            transaction_id=transaction_id,
            subcategory_id=subcategory_id,
            raw_input=raw_input,
            source_type=source_type,
            confidence_score=float(confidence_score),
            created_at=now_str
        )

    def get_transaction_metadata(self, transaction_id: str) -> Optional[TransactionMetadata]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transaction_metadata WHERE transaction_id = ?", (transaction_id,))
        r = cur.fetchone()
        if not r:
            return None
        return TransactionMetadata(
            transaction_id=r["transaction_id"],
            subcategory_id=r["subcategory_id"],
            raw_input=r["raw_input"],
            source_type=r["source_type"],
            confidence_score=float(r["confidence_score"]),
            created_at=r["created_at"]
        )

    def record_correction_event(
        self,
        transaction_id: str,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
        reason: Optional[str] = None
    ) -> CorrectionEvent:
        conn = self.db.get_connection()
        corr_id = self._generate_id("corr")
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                """INSERT INTO correction_events (id, transaction_id, field_name, old_value, new_value, reason, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (corr_id, transaction_id, field_name, str(old_value) if old_value is not None else None,
                 str(new_value) if new_value is not None else None, reason, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "correction_events", corr_id, "CREATE", now_str)
            )
        return CorrectionEvent(
            id=corr_id,
            transaction_id=transaction_id,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            reason=reason,
            created_at=now_str
        )

    def list_correction_events(self, transaction_id: Optional[str] = None) -> List[CorrectionEvent]:
        conn = self.db.get_connection()
        query = "SELECT * FROM correction_events"
        params = []
        if transaction_id:
            query += " WHERE transaction_id = ?"
            params.append(transaction_id)
        query += " ORDER BY created_at DESC"
        cur = conn.execute(query, params)
        return [
            CorrectionEvent(
                id=r["id"],
                transaction_id=r["transaction_id"],
                field_name=r["field_name"],
                old_value=r["old_value"],
                new_value=r["new_value"],
                reason=r["reason"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    def correct_transaction(
        self,
        transaction_id: str,
        account_id: Optional[str] = None,
        amount: Optional[float] = None,
        direction: Optional[str] = None,
        category_id: Optional[str] = None,
        note: Optional[str] = None,
        tx_date: Optional[str] = None,
        reason: str = "Owner correction",
        subcategory_id: Optional[str] = None,
        scope: str = "transaction"
    ) -> Transaction:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        old_tx = cur.fetchone()
        if not old_tx:
            raise ValueError(f"Transaction {transaction_id} not found")

        keys = old_tx.keys()
        old_acc_id = old_tx["account_id"]
        old_amount = float(old_tx["amount"])
        old_dir = old_tx["direction"]
        old_cat_id = old_tx["category_id"]
        old_subcat_id = old_tx["subcategory_id"] if "subcategory_id" in keys else None
        old_note = old_tx["note"]
        old_date = old_tx["date"]

        new_acc_id = account_id if account_id is not None else old_acc_id
        new_amount = float(amount) if amount is not None else old_amount
        new_dir = direction.upper() if direction is not None else old_dir
        new_cat_id = category_id if category_id is not None else old_cat_id
        new_subcat_id = subcategory_id if subcategory_id is not None else old_subcat_id
        new_note = note if note is not None else old_note
        new_date = tx_date if tx_date is not None else old_date

        if new_subcat_id:
            sub_cur = conn.execute("SELECT * FROM subcategories WHERE id = ?", (new_subcat_id,))
            sub_row = sub_cur.fetchone()
            if sub_row and new_cat_id and sub_row["category_id"] != new_cat_id:
                raise ValueError(f"Subcategory {new_subcat_id} does not belong to category {new_cat_id}")

        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            # Revert old balance effect
            if old_dir == "EXPENSE":
                conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (old_amount, old_acc_id))
            elif old_dir == "INCOME":
                conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (old_amount, old_acc_id))

            # Apply new balance effect
            if new_dir == "EXPENSE":
                conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (new_amount, new_acc_id))
            elif new_dir == "INCOME":
                conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (new_amount, new_acc_id))

            # Update transaction
            conn.execute(
                """UPDATE transactions 
                   SET account_id = ?, amount = ?, direction = ?, category_id = ?, subcategory_id = ?, note = ?, date = ?, status = 'CORRECTED', updated_at = ?
                   WHERE id = ?""",
                (new_acc_id, new_amount, new_dir, new_cat_id, new_subcat_id, new_note, new_date, now_str, transaction_id)
            )

            # Record correction events for changes
            if new_acc_id != old_acc_id:
                self.record_correction_event(transaction_id, "account_id", old_acc_id, new_acc_id, reason)
            if new_amount != old_amount:
                self.record_correction_event(transaction_id, "amount", str(old_amount), str(new_amount), reason)
            if new_dir != old_dir:
                self.record_correction_event(transaction_id, "direction", old_dir, new_dir, reason)
            if new_cat_id != old_cat_id:
                self.record_correction_event(transaction_id, "category_id", old_cat_id, new_cat_id, reason)
            if new_subcat_id != old_subcat_id:
                self.record_correction_event(transaction_id, "subcategory_id", old_subcat_id, new_subcat_id, reason)
            if new_note != old_note:
                self.record_correction_event(transaction_id, "note", old_note, new_note, reason)
            if new_date != old_date:
                self.record_correction_event(transaction_id, "date", old_date, new_date, reason)

            if new_subcat_id:
                self.record_transaction_metadata(transaction_id, subcategory_id=new_subcat_id)

            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "transactions", transaction_id, "CORRECT", now_str)
            )

        cur = conn.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        return self._transaction_from_row(cur.fetchone())

    def void_transaction(
        self,
        transaction_id: str,
        reason: str = "Voided by owner",
        scope: str = "transaction"
    ) -> Dict[str, Any]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        tx = cur.fetchone()
        if not tx:
            raise ValueError(f"Transaction {transaction_id} not found")

        keys = tx.keys()
        t_status = tx["status"] if "status" in keys and tx["status"] else "ACTIVE"
        if t_status == "VOID":
            return {"success": True, "atomic": True, "voided_ids": [transaction_id]}

        target_txs = [tx]

        # If scope == 'event' or transfer, find paired transfer
        if (scope == "event" or tx["direction"] == "TRANSFER") and tx["direction"] == "TRANSFER":
            opp_cur = conn.execute(
                """SELECT * FROM transactions 
                   WHERE id != ? AND direction = 'TRANSFER' AND amount = ? AND date = ? 
                     AND (status IS NULL OR status != 'VOID')
                   ORDER BY ABS(strftime('%s', created_at) - strftime('%s', ?)) ASC
                   LIMIT 1""",
                (transaction_id, tx["amount"], tx["date"], tx["created_at"])
            )
            peer_row = opp_cur.fetchone()
            if peer_row:
                target_txs.append(peer_row)

        now_str = datetime.now(timezone.utc).isoformat()
        voided_ids = []

        with conn:
            for t in target_txs:
                t_id = t["id"]
                t_acc_id = t["account_id"]
                t_amount = float(t["amount"])
                t_dir = t["direction"]
                t_note = t["note"] or ""
                curr_status = t["status"] if "status" in t.keys() and t["status"] else "ACTIVE"

                # Reverse balance effect
                if t_dir == "EXPENSE":
                    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (t_amount, t_acc_id))
                elif t_dir == "INCOME":
                    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (t_amount, t_acc_id))
                elif t_dir == "TRANSFER":
                    if t_note.startswith("Transfer ke "):
                        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (t_amount, t_acc_id))
                    elif t_note.startswith("Transfer dari "):
                        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (t_amount, t_acc_id))
                    else:
                        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (t_amount, t_acc_id))

                # Update transaction status
                conn.execute(
                    """UPDATE transactions 
                       SET status = 'VOID', voided_at = ?, void_reason = ?, updated_at = ?
                       WHERE id = ?""",
                    (now_str, reason, now_str, t_id)
                )

                # Record audit log
                audit_id = self._generate_id("aud")
                conn.execute(
                    "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                    (audit_id, "transactions", t_id, "VOID", now_str)
                )

                # Record correction event
                self.record_correction_event(t_id, "status", curr_status, "VOID", reason)
                voided_ids.append(t_id)

        return {
            "success": True,
            "atomic": True,
            "voided_ids": voided_ids
        }

    def delete_credit_card(self, card_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM credit_cards WHERE id = ?", (card_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            stmts = conn.execute("SELECT COUNT(*) FROM credit_card_statements WHERE card_id = ?", (card_id,)).fetchone()[0]
            pmts = conn.execute("SELECT COUNT(*) FROM credit_card_payments WHERE card_id = ?", (card_id,)).fetchone()[0]
            if stmts > 0 or pmts > 0:
                conn.execute("UPDATE credit_cards SET is_active = 0, updated_at = ? WHERE id = ?", (now_str, card_id))
            else:
                conn.execute("DELETE FROM credit_cards WHERE id = ?", (card_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_cards", card_id, "DELETE", now_str)
            )
        return True

    def delete_subcategory(self, subcategory_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM subcategories WHERE id = ?", (subcategory_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            tx_count = conn.execute("SELECT COUNT(*) FROM transactions WHERE subcategory_id = ?", (subcategory_id,)).fetchone()[0]
            if tx_count > 0:
                conn.execute("UPDATE subcategories SET is_active = 0 WHERE id = ?", (subcategory_id,))
            else:
                conn.execute("DELETE FROM subcategories WHERE id = ?", (subcategory_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "subcategories", subcategory_id, "DELETE", now_str)
            )
        return True

    def delete_category(self, category_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            tx_count = conn.execute("SELECT COUNT(*) FROM transactions WHERE category_id = ?", (category_id,)).fetchone()[0]
            sub_count = conn.execute("SELECT COUNT(*) FROM subcategories WHERE category_id = ?", (category_id,)).fetchone()[0]
            if tx_count > 0 or sub_count > 0:
                conn.execute("UPDATE categories SET is_active = 0 WHERE id = ?", (category_id,))
            else:
                conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "categories", category_id, "DELETE", now_str)
            )
        return True

    def delete_account(self, account_id: str) -> bool:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        if not cur.fetchone():
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            tx_count = conn.execute("SELECT COUNT(*) FROM transactions WHERE account_id = ?", (account_id,)).fetchone()[0]
            if tx_count > 0:
                conn.execute("UPDATE accounts SET is_active = 0 WHERE id = ?", (account_id,))
            else:
                conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "accounts", account_id, "DELETE", now_str)
            )
        return True

    # ====================================================
    # Phase 3.1: Review Queue
    # ====================================================
    def enqueue_review_item(
        self,
        raw_text: str,
        parsed_result: Dict[str, Any],
        confidence: float = 1.0,
        issue_reason: Optional[str] = None
    ) -> ReviewQueueItem:
        import json
        conn = self.db.get_connection()
        item_id = self._generate_id("rq")
        now_str = datetime.now(timezone.utc).isoformat()
        parsed_json = json.dumps(parsed_result)
        with conn:
            conn.execute(
                """INSERT INTO review_queue (id, raw_text, parsed_result, confidence, issue_reason, status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 'PENDING', ?, ?)""",
                (item_id, raw_text, parsed_json, float(confidence), issue_reason, now_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "review_queue", item_id, "ENQUEUE", now_str)
            )
        return ReviewQueueItem(
            id=item_id,
            raw_text=raw_text,
            parsed_result=parsed_json,
            confidence=float(confidence),
            issue_reason=issue_reason,
            status="PENDING",
            approved_transaction_id=None,
            created_at=now_str,
            updated_at=now_str
        )

    def list_review_queue(self, status: Optional[str] = None) -> List[ReviewQueueItem]:
        conn = self.db.get_connection()
        query = "SELECT * FROM review_queue"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status.upper())
        query += " ORDER BY created_at DESC"
        cur = conn.execute(query, params)
        return [
            ReviewQueueItem(
                id=r["id"],
                raw_text=r["raw_text"],
                parsed_result=r["parsed_result"],
                confidence=float(r["confidence"]),
                issue_reason=r["issue_reason"],
                status=r["status"],
                approved_transaction_id=r["approved_transaction_id"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in cur.fetchall()
        ]

    def get_review_queue_item(self, item_id: str) -> Optional[ReviewQueueItem]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM review_queue WHERE id = ?", (item_id,))
        r = cur.fetchone()
        if not r:
            return None
        return ReviewQueueItem(
            id=r["id"],
            raw_text=r["raw_text"],
            parsed_result=r["parsed_result"],
            confidence=float(r["confidence"]),
            issue_reason=r["issue_reason"],
            status=r["status"],
            approved_transaction_id=r["approved_transaction_id"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    def approve_review_item(self, item_id: str, override_data: Optional[Dict[str, Any]] = None) -> Tuple[ReviewQueueItem, Transaction]:
        import json
        item = self.get_review_queue_item(item_id)
        if not item:
            raise ValueError(f"Review item {item_id} not found")
        if item.status != "PENDING":
            raise ValueError(f"Review item {item_id} is already {item.status}")
        
        parsed = json.loads(item.parsed_result)
        if override_data:
            parsed.update(override_data)
            
        account_id = parsed["account_id"]
        amount = float(parsed["amount"])
        direction = parsed.get("direction", "EXPENSE")
        category_id = parsed.get("category_id")
        note = parsed.get("note", item.raw_text)
        subcategory_id = parsed.get("subcategory_id")
        tx_date = parsed.get("date")
        
        if direction == "TRANSFER":
            dst_acc_id = None
            if override_data and override_data.get("destination_account_id"):
                dst_acc_id = override_data["destination_account_id"]
            elif parsed.get("destination_account_id"):
                dst_acc_id = parsed["destination_account_id"]

            conn = self.db.get_connection()
            if not dst_acc_id:
                dst_name = (override_data.get("destination_account_name") if override_data else None) or parsed.get("destination_account_name") or "Internal transfer"
                dst_row = conn.execute("SELECT id FROM accounts WHERE (name = ? OR name LIKE ?) AND id != ? LIMIT 1", (dst_name, f"%{dst_name}%", account_id)).fetchone()
                if dst_row:
                    dst_acc_id = dst_row["id"]
                else:
                    pocket_row = conn.execute("SELECT id FROM accounts WHERE (parent_account_id = ? OR type = 'POCKET' OR name LIKE '%saving%') AND id != ? LIMIT 1", (account_id, account_id)).fetchone()
                    if pocket_row:
                        dst_acc_id = pocket_row["id"]
                    else:
                        new_pocket = self.create_account(
                            name="Internal transfer",
                            account_type="POCKET",
                            initial_balance=0.0,
                            account_class="POCKET",
                            dashboard_group="CASH",
                            parent_account_id=account_id
                        )
                        dst_acc_id = new_pocket.id

            tx_out, tx_in = self.transfer_funds(
                source_account_id=account_id,
                destination_account_id=dst_acc_id,
                amount=amount,
                note=note,
                source="REVIEW_QUEUE",
                tx_date=tx_date
            )
            tx = tx_out
        else:
            tx = self.create_transaction(
                account_id=account_id,
                amount=amount,
                direction=direction,
                category_id=category_id,
                subcategory_id=subcategory_id,
                note=note,
                source="REVIEW_QUEUE",
                tx_date=tx_date
            )
            self.record_transaction_metadata(
                transaction_id=tx.id,
                subcategory_id=subcategory_id,
                raw_input=item.raw_text,
                source_type="REVIEW_QUEUE",
                confidence_score=item.confidence
            )
        
        # Learning system (Phase 7): If owner corrects or confirms merchant alias, persist to category_aliases
        if override_data:
            kw = override_data.get("alias_keyword") or override_data.get("merchant") or parsed.get("note")
            if kw and category_id:
                try:
                    self.add_category_alias(
                        keyword=kw.strip(),
                        subcategory_id=subcategory_id,
                        category_id=category_id,
                        priority=10
                    )
                except Exception:
                    pass

        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                "UPDATE review_queue SET status = 'APPROVED', approved_transaction_id = ?, updated_at = ? WHERE id = ?",
                (tx.id, now_str, item_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "review_queue", item_id, "APPROVE", now_str)
            )
            
        updated_item = self.get_review_queue_item(item_id)
        return updated_item, tx

    def reject_review_item(self, item_id: str, reason: Optional[str] = None) -> Optional[ReviewQueueItem]:
        item = self.get_review_queue_item(item_id)
        if not item:
            return None
        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        issue = f"{item.issue_reason or ''} | Rejected: {reason}".strip(" |") if reason else item.issue_reason
        with conn:
            conn.execute(
                "UPDATE review_queue SET status = 'REJECTED', issue_reason = ?, updated_at = ? WHERE id = ?",
                (issue, now_str, item_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "review_queue", item_id, "REJECT", now_str)
            )
        return self.get_review_queue_item(item_id)

    def ignore_review_item(self, item_id: str, reason: Optional[str] = None) -> Optional[ReviewQueueItem]:
        item = self.get_review_queue_item(item_id)
        if not item:
            return None
        conn = self.db.get_connection()
        now_str = datetime.now(timezone.utc).isoformat()
        issue = f"{item.issue_reason or ''} | Ignored: {reason}".strip(" |") if reason else (item.issue_reason or "Abaikan")
        with conn:
            conn.execute(
                "UPDATE review_queue SET status = 'IGNORED', issue_reason = ?, updated_at = ? WHERE id = ?",
                (issue, now_str, item_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "review_queue", item_id, "IGNORE", now_str)
            )
        return self.get_review_queue_item(item_id)

    def get_finance_inbox(self) -> Dict[str, Any]:
        """
        Groups review queue candidates into 4 sections:
        - new_candidates: PENDING with confidence >= 0.70
        - needs_review: PENDING with confidence < 0.70
        - approved: status = APPROVED
        - ignored: status in ('IGNORED', 'REJECTED')
        """
        import json
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM review_queue ORDER BY created_at DESC")
        rows = cur.fetchall()

        new_candidates = []
        needs_review = []
        approved = []
        ignored = []

        for r in rows:
            parsed = json.loads(r["parsed_result"]) if r["parsed_result"] else {}
            item = {
                "id": r["id"],
                "raw_text": r["raw_text"],
                "parsed": parsed,
                "confidence": float(r["confidence"]),
                "issue_reason": r["issue_reason"],
                "status": r["status"],
                "approved_transaction_id": r["approved_transaction_id"],
                "created_at": r["created_at"],
                "updated_at": r["updated_at"]
            }
            st = r["status"]
            if st == "PENDING":
                if float(r["confidence"]) >= 0.70:
                    new_candidates.append(item)
                else:
                    needs_review.append(item)
            elif st == "APPROVED":
                approved.append(item)
            elif st in ("IGNORED", "REJECTED"):
                ignored.append(item)

        return {
            "counts": {
                "new_candidates": len(new_candidates),
                "needs_review": len(needs_review),
                "approved": len(approved),
                "ignored": len(ignored),
                "total_pending": len(new_candidates) + len(needs_review)
            },
            "new_candidates": new_candidates,
            "needs_review": needs_review,
            "approved": approved,
            "ignored": ignored
        }

    # ====================================================
    # Phase 3.1: Credit Cards
    # ====================================================
    def create_credit_card(
        self,
        name: str,
        bank_name: str,
        credit_limit: float,
        account_id: Optional[str] = None,
        billing_cycle_day: int = 1,
        payment_due_day: int = 15
    ) -> CreditCard:
        conn = self.db.get_connection()
        card_id = self._generate_id("cc")
        now_str = datetime.now(timezone.utc).isoformat()
        clean_name = name.strip()
        clean_bank = bank_name.strip()
        if not clean_name or not clean_bank:
            raise ValueError("Card name and bank name cannot be empty")
        if not account_id:
            cc_acc = self.create_account(
                name=f"CC - {clean_name}",
                account_type="BANK",
                initial_balance=0.0,
                provider=clean_bank,
                account_class="LIABILITY",
                dashboard_group="CREDIT_CARD"
            )
            account_id = cc_acc.id
        with conn:
            conn.execute(
                """INSERT INTO credit_cards (id, account_id, name, bank_name, credit_limit, current_balance, billing_cycle_day, payment_due_day, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 0.0, ?, ?, 1, ?, ?)""",
                (card_id, account_id, clean_name, clean_bank, float(credit_limit), int(billing_cycle_day), int(payment_due_day), now_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_cards", card_id, "CREATE", now_str)
            )
        return CreditCard(
            id=card_id,
            account_id=account_id,
            name=clean_name,
            bank_name=clean_bank,
            credit_limit=float(credit_limit),
            current_balance=0.0,
            billing_cycle_day=int(billing_cycle_day),
            payment_due_day=int(payment_due_day),
            is_active=1,
            created_at=now_str,
            updated_at=now_str
        )

    def get_credit_card(self, card_id: str) -> Optional[CreditCard]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM credit_cards WHERE id = ?", (card_id,))
        r = cur.fetchone()
        if not r:
            return None
        return CreditCard(
            id=r["id"],
            account_id=r["account_id"],
            name=r["name"],
            bank_name=r["bank_name"],
            credit_limit=float(r["credit_limit"]),
            current_balance=float(r["current_balance"]),
            billing_cycle_day=int(r["billing_cycle_day"]),
            payment_due_day=int(r["payment_due_day"]),
            is_active=int(r["is_active"]),
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    def list_credit_cards(self, active_only: bool = False) -> List[CreditCard]:
        conn = self.db.get_connection()
        query = "SELECT * FROM credit_cards"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name ASC"
        cur = conn.execute(query)
        return [
            CreditCard(
                id=r["id"],
                account_id=r["account_id"],
                name=r["name"],
                bank_name=r["bank_name"],
                credit_limit=float(r["credit_limit"]),
                current_balance=float(r["current_balance"]),
                billing_cycle_day=int(r["billing_cycle_day"]),
                payment_due_day=int(r["payment_due_day"]),
                is_active=int(r["is_active"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in cur.fetchall()
        ]

    def update_credit_card(
        self,
        card_id: str,
        name: Optional[str] = None,
        bank_name: Optional[str] = None,
        credit_limit: Optional[float] = None,
        current_balance: Optional[float] = None,
        billing_cycle_day: Optional[int] = None,
        payment_due_day: Optional[int] = None,
        is_active: Optional[int] = None
    ) -> Optional[CreditCard]:
        card = self.get_credit_card(card_id)
        if not card:
            return None
        new_name = name.strip() if name is not None else card.name
        new_bank = bank_name.strip() if bank_name is not None else card.bank_name
        new_limit = float(credit_limit) if credit_limit is not None else card.credit_limit
        new_bal = float(current_balance) if current_balance is not None else card.current_balance
        new_cycle = int(billing_cycle_day) if billing_cycle_day is not None else card.billing_cycle_day
        new_due = int(payment_due_day) if payment_due_day is not None else card.payment_due_day
        new_active = int(is_active) if is_active is not None else card.is_active
        now_str = datetime.now(timezone.utc).isoformat()
        conn = self.db.get_connection()
        with conn:
            conn.execute(
                """UPDATE credit_cards 
                   SET name = ?, bank_name = ?, credit_limit = ?, current_balance = ?, billing_cycle_day = ?, payment_due_day = ?, is_active = ?, updated_at = ?
                   WHERE id = ?""",
                (new_name, new_bank, new_limit, new_bal, new_cycle, new_due, new_active, now_str, card_id)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_cards", card_id, "UPDATE", now_str)
            )
        return self.get_credit_card(card_id)

    def create_credit_card_statement(
        self,
        card_id: str,
        statement_period: str,
        statement_date: str,
        due_date: str,
        total_amount: float,
        minimum_payment: float = 0.0
    ) -> CreditCardStatement:
        conn = self.db.get_connection()
        stmt_id = self._generate_id("stmt")
        now_str = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute(
                """INSERT INTO credit_card_statements (id, card_id, statement_period, statement_date, due_date, total_amount, minimum_payment, unpaid_amount, status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'UNPAID', ?, ?)""",
                (stmt_id, card_id, statement_period, statement_date, due_date, float(total_amount), float(minimum_payment), float(total_amount), now_str, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_card_statements", stmt_id, "CREATE", now_str)
            )
        return CreditCardStatement(
            id=stmt_id,
            card_id=card_id,
            statement_period=statement_period,
            statement_date=statement_date,
            due_date=due_date,
            total_amount=float(total_amount),
            minimum_payment=float(minimum_payment),
            unpaid_amount=float(total_amount),
            status="UNPAID",
            created_at=now_str,
            updated_at=now_str
        )

    def list_credit_card_statements(self, card_id: Optional[str] = None) -> List[CreditCardStatement]:
        conn = self.db.get_connection()
        query = "SELECT * FROM credit_card_statements"
        params = []
        if card_id:
            query += " WHERE card_id = ?"
            params.append(card_id)
        query += " ORDER BY due_date DESC"
        cur = conn.execute(query, params)
        return [
            CreditCardStatement(
                id=r["id"],
                card_id=r["card_id"],
                statement_period=r["statement_period"],
                statement_date=r["statement_date"],
                due_date=r["due_date"],
                total_amount=float(r["total_amount"]),
                minimum_payment=float(r["minimum_payment"]),
                unpaid_amount=float(r["unpaid_amount"]),
                status=r["status"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in cur.fetchall()
        ]

    def record_credit_card_payment(
        self,
        card_id: str,
        payment_date: str,
        amount: float,
        statement_id: Optional[str] = None,
        transaction_id: Optional[str] = None,
        notes: Optional[str] = None,
        account_id: Optional[str] = None
    ) -> CreditCardPayment:
        conn = self.db.get_connection()
        pmt_id = self._generate_id("ccpay")
        now_str = datetime.now(timezone.utc).isoformat()
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Payment amount must be positive")

        cur_card = conn.execute("SELECT * FROM credit_cards WHERE id = ?", (card_id,)).fetchone()
        if not cur_card:
            raise ValueError(f"Credit card not found: {card_id}")
        card_name = cur_card["name"]

        with conn:
            # 1. Deduct cash account if specified
            if account_id:
                cur_acc = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
                if not cur_acc:
                    raise ValueError(f"Payment cash account not found: {account_id}")
                new_acc_bal = float(cur_acc["balance"]) - amt
                conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_acc_bal, account_id))

                if not transaction_id:
                    tx_id = self._generate_id("tx")
                    pmt_note = notes or f"Pembayaran CC {card_name}"
                    conn.execute(
                        """INSERT INTO transactions 
                           (id, date, account_id, category_id, amount, direction, note, source, status, created_at, updated_at) 
                           VALUES (?, ?, ?, NULL, ?, 'TRANSFER', ?, 'CREDIT_CARD_PAYMENT', 'ACTIVE', ?, ?)""",
                        (tx_id, payment_date, account_id, amt, pmt_note, now_str, now_str)
                    )
                    transaction_id = tx_id

            # 2. Record payment in credit_card_payments
            conn.execute(
                """INSERT INTO credit_card_payments (id, card_id, statement_id, transaction_id, payment_date, amount, notes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (pmt_id, card_id, statement_id, transaction_id, payment_date, amt, notes, now_str)
            )

            # 3. Update statement unpaid balance if statement_id provided
            if statement_id:
                cur = conn.execute("SELECT unpaid_amount FROM credit_card_statements WHERE id = ?", (statement_id,))
                stmt_row = cur.fetchone()
                if stmt_row:
                    new_unpaid = max(0.0, float(stmt_row["unpaid_amount"]) - amt)
                    new_status = "PAID" if new_unpaid == 0 else "PARTIALLY_PAID"
                    conn.execute(
                        "UPDATE credit_card_statements SET unpaid_amount = ?, status = ?, updated_at = ? WHERE id = ?",
                        (new_unpaid, new_status, now_str, statement_id)
                    )

            # 4. Reduce credit card liability
            new_card_bal = max(0.0, float(cur_card["current_balance"]) - amt)
            conn.execute(
                "UPDATE credit_cards SET current_balance = ?, updated_at = ? WHERE id = ?",
                (new_card_bal, now_str, card_id)
            )

            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_card_payments", pmt_id, "CREATE", now_str)
            )
        return CreditCardPayment(
            id=pmt_id,
            card_id=card_id,
            statement_id=statement_id,
            transaction_id=transaction_id,
            payment_date=payment_date,
            amount=amt,
            notes=notes,
            created_at=now_str
        )

    def list_credit_card_payments(self, card_id: Optional[str] = None) -> List[CreditCardPayment]:
        conn = self.db.get_connection()
        query = "SELECT * FROM credit_card_payments"
        params = []
        if card_id:
            query += " WHERE card_id = ?"
            params.append(card_id)
        query += " ORDER BY payment_date DESC"
        cur = conn.execute(query, params)
        return [
            CreditCardPayment(
                id=r["id"],
                card_id=r["card_id"],
                statement_id=r["statement_id"],
                transaction_id=r["transaction_id"],
                payment_date=r["payment_date"],
                amount=float(r["amount"]),
                notes=r["notes"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    def get_credit_card_summary(self, card_id: str) -> Dict[str, Any]:
        card = self.get_credit_card(card_id)
        if not card:
            raise ValueError(f"Credit card not found: {card_id}")
        statements = self.list_credit_card_statements(card_id)
        payments = self.list_credit_card_payments(card_id)
        billed_unpaid = sum(s.unpaid_amount for s in statements if s.status != "PAID")
        latest_stmt = statements[0] if statements else None
        unbilled_amount = max(0.0, card.current_balance - billed_unpaid)
        return {
            "card_id": card.id,
            "name": card.name,
            "bank_name": card.bank_name,
            "credit_limit": card.credit_limit,
            "current_balance": card.current_balance,
            "available_credit": max(0.0, card.credit_limit - card.current_balance),
            "billing_cycle_day": card.billing_cycle_day,
            "payment_due_day": card.payment_due_day,
            "statement_balance": latest_stmt.unpaid_amount if latest_stmt else 0.0,
            "unbilled_amount": unbilled_amount,
            "closed_statements": [
                {
                    "id": s.id,
                    "statement_period": s.statement_period,
                    "statement_date": s.statement_date,
                    "due_date": s.due_date,
                    "total_amount": s.total_amount,
                    "unpaid_amount": s.unpaid_amount,
                    "status": s.status
                }
                for s in statements
            ],
            "payment_history": [
                {
                    "id": p.id,
                    "payment_date": p.payment_date,
                    "amount": p.amount,
                    "statement_id": p.statement_id,
                    "notes": p.notes
                }
                for p in payments
            ],
            "payment_history_count": len(payments)
        }

    # ====================================================
    # Phase 3.1: Liability Payments
    # ====================================================
    def record_liability_payment(
        self,
        liability_id: str,
        payment_date: str,
        amount: float,
        principal_portion: float = 0.0,
        interest_portion: float = 0.0,
        transaction_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> LiabilityPayment:
        conn = self.db.get_connection()
        pmt_id = self._generate_id("lpay")
        now_str = datetime.now(timezone.utc).isoformat()
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Liability payment amount must be positive")
        princ = float(principal_portion) if principal_portion > 0 else amt
        with conn:
            conn.execute(
                """INSERT INTO liability_payments (id, liability_id, payment_date, amount, principal_portion, interest_portion, transaction_id, notes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (pmt_id, liability_id, payment_date, amt, float(principal_portion), float(interest_portion), transaction_id, notes, now_str)
            )
            cur = conn.execute("SELECT remaining_amount FROM liabilities WHERE id = ?", (liability_id,))
            liab_row = cur.fetchone()
            if liab_row:
                new_rem = max(0.0, float(liab_row["remaining_amount"]) - princ)
                conn.execute(
                    "UPDATE liabilities SET remaining_amount = ?, updated_at = ? WHERE id = ?",
                    (new_rem, now_str, liability_id)
                )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "liability_payments", pmt_id, "CREATE", now_str)
            )
        return LiabilityPayment(
            id=pmt_id,
            liability_id=liability_id,
            payment_date=payment_date,
            amount=amt,
            principal_portion=float(principal_portion),
            interest_portion=float(interest_portion),
            transaction_id=transaction_id,
            notes=notes,
            created_at=now_str
        )

    def list_liability_payments(self, liability_id: Optional[str] = None) -> List[LiabilityPayment]:
        conn = self.db.get_connection()
        query = "SELECT * FROM liability_payments"
        params = []
        if liability_id:
            query += " WHERE liability_id = ?"
            params.append(liability_id)
        query += " ORDER BY payment_date DESC"
        cur = conn.execute(query, params)
        return [
            LiabilityPayment(
                id=r["id"],
                liability_id=r["liability_id"],
                payment_date=r["payment_date"],
                amount=float(r["amount"]),
                principal_portion=float(r["principal_portion"]),
                interest_portion=float(r["interest_portion"]),
                transaction_id=r["transaction_id"],
                notes=r["notes"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    # ====================================================
    # Phase 3.1: Asset Valuations
    # ====================================================
    def record_asset_valuation(
        self,
        asset_id: str,
        valuation_date: str,
        value: Optional[float] = None,
        unit_price: Optional[float] = None,
        reason: Optional[str] = None
    ) -> AssetValuation:
        conn = self.db.get_connection()
        ast_row = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
        if not ast_row:
            raise ValueError(f"Asset not found: {asset_id}")

        val_id = self._generate_id("aval")
        now_str = datetime.now(timezone.utc).isoformat()

        if unit_price is not None:
            unit_p = float(unit_price)
            wt = float(ast_row["weight_grams"]) if ast_row["weight_grams"] is not None and float(ast_row["weight_grams"]) > 0 else 1.0
            val = unit_p * wt if value is None else float(value)
        elif value is not None:
            val = float(value)
            unit_p = None
        else:
            raise ValueError("Either value or unit_price must be provided")

        if val < 0:
            raise ValueError("Asset value cannot be negative")

        cols = [c[1] for c in conn.execute("PRAGMA table_info(assets)").fetchall()]
        with conn:
            conn.execute(
                """INSERT INTO asset_valuation_history (id, asset_id, valuation_date, value, reason, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (val_id, asset_id, valuation_date, val, reason, now_str)
            )
            if unit_p is not None and "current_unit_price" in cols:
                conn.execute(
                    "UPDATE assets SET current_value = ?, current_unit_price = ?, updated_at = ? WHERE id = ?",
                    (val, unit_p, now_str, asset_id)
                )
            else:
                conn.execute(
                    "UPDATE assets SET current_value = ?, updated_at = ? WHERE id = ?",
                    (val, now_str, asset_id)
                )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "asset_valuation_history", val_id, "CREATE", now_str)
            )
        return AssetValuation(
            id=val_id,
            asset_id=asset_id,
            valuation_date=valuation_date,
            value=val,
            reason=reason,
            created_at=now_str
        )

    def list_asset_valuations(self, asset_id: Optional[str] = None) -> List[AssetValuation]:
        conn = self.db.get_connection()
        query = "SELECT * FROM asset_valuation_history"
        params = []
        if asset_id:
            query += " WHERE asset_id = ?"
            params.append(asset_id)
        query += " ORDER BY valuation_date DESC"
        cur = conn.execute(query, params)
        return [
            AssetValuation(
                id=r["id"],
                asset_id=r["asset_id"],
                valuation_date=r["valuation_date"],
                value=float(r["value"]),
                reason=r["reason"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

    # ====================================================
    # Domain Alignment V2 Methods
    # ====================================================
    def internal_pocket_transfer(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        notes: Optional[str] = None,
        tx_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transfers funds between physical accounts and/or internal pockets.
        Does NOT change total liquid cash, net worth, income, or expense.
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than 0")
        if from_account_id == to_account_id:
            raise ValueError("Source and destination accounts must be different")

        note_txt = f"Pocket Transfer: {notes}" if notes else "Internal Pocket Transfer"
        tx_out, tx_in = self.transfer_funds(
            source_account_id=from_account_id,
            destination_account_id=to_account_id,
            amount=amount,
            note=note_txt,
            source="POCKET_TRANSFER",
            tx_date=tx_date
        )
        return {
            "success": True,
            "amount": amount,
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "tx_out_id": tx_out.id,
            "tx_in_id": tx_in.id,
            "note": note_txt
        }

    def record_asset_purchase(
        self,
        account_id: str,
        asset_id: str,
        amount: float,
        notes: Optional[str] = None,
        tx_date: Optional[str] = None,
        weight_grams: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Records an asset purchase (e.g. buying gold):
        - Cash account is deducted
        - Asset current_value and purchase_cost increase by amount
        - Direction is 'ASSET_PURCHASE' (tracked in ledger, NOT an expense)
        - Net worth is preserved (Cash down, Asset up by same amount)
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Purchase amount must be greater than 0")

        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        acc = cur.fetchone()
        if not acc:
            raise ValueError(f"Account not found: {account_id}")

        cur = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
        ast = cur.fetchone()
        if not ast:
            raise ValueError(f"Asset not found: {asset_id}")

        tx_id = self._generate_id("tx")
        now_str = datetime.now(timezone.utc).isoformat()
        if not tx_date:
            tx_date = date.today().isoformat()

        user_notes = notes or f"Pembelian Aset: {ast['name']}"
        new_acc_bal = float(acc["balance"]) - amount
        new_ast_val = float(ast["current_value"]) + amount

        # Check asset columns
        cols = [c[1] for c in conn.execute("PRAGMA table_info(assets)").fetchall()]
        ast_dict = dict(ast)
        curr_pc = float(ast_dict.get("purchase_cost") or 0.0)
        curr_wt = float(ast_dict.get("weight_grams") or 0.0)
        new_purchase_cost = curr_pc + amount
        new_weight = (curr_wt + float(weight_grams)) if weight_grams else curr_wt
        new_avg_cost = round(new_purchase_cost / new_weight, 2) if new_weight > 0 else 0.0
        new_unit_price = float(ast_dict.get("current_unit_price") or 0.0)
        if new_unit_price == 0.0 and new_weight > 0:
            new_unit_price = round(new_ast_val / new_weight, 2)

        with conn:
            # 1. Deduct cash account
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_acc_bal, account_id))

            # 2. Update asset value and details
            if "weight_grams" in cols:
                conn.execute(
                    """UPDATE assets 
                       SET current_value = ?, purchase_cost = ?, weight_grams = ?, average_cost_per_gram = ?, current_unit_price = ?, updated_at = ? 
                       WHERE id = ?""",
                    (new_ast_val, new_purchase_cost, new_weight, new_avg_cost, new_unit_price, now_str, asset_id)
                )
            else:
                conn.execute(
                    "UPDATE assets SET current_value = ?, updated_at = ? WHERE id = ?",
                    (new_ast_val, now_str, asset_id)
                )

            # 3. Insert transaction with direction='ASSET_PURCHASE'
            conn.execute(
                """INSERT INTO transactions 
                   (id, date, account_id, category_id, amount, direction, note, source, status, created_at, updated_at) 
                   VALUES (?, ?, ?, NULL, ?, 'ASSET_PURCHASE', ?, 'ASSET_PURCHASE', 'ACTIVE', ?, ?)""",
                (tx_id, tx_date, account_id, amount, user_notes, now_str, now_str)
            )

            # 4. Record valuation entry
            val_id = self._generate_id("aval")
            conn.execute(
                """INSERT INTO asset_valuation_history (id, asset_id, valuation_date, value, reason, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (val_id, asset_id, tx_date, new_ast_val, f"Asset purchase: {user_notes}", now_str)
            )

            # 5. Audit logs
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "assets", asset_id, "PURCHASE", now_str)
            )

        return {
            "success": True,
            "transaction_id": tx_id,
            "account_id": account_id,
            "asset_id": asset_id,
            "amount": amount,
            "new_account_balance": new_acc_bal,
            "new_asset_value": new_ast_val
        }

    def record_credit_card_purchase(
        self,
        card_id: str,
        amount: float,
        category_id: Optional[str] = None,
        subcategory_id: Optional[str] = None,
        note: Optional[str] = None,
        tx_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Records a credit card purchase flow:
        - Cash is UNCHANGED (0 deduction from bank accounts)
        - Credit card liability (current_balance) increases by amount
        - Direction is 'EXPENSE' (classified as expense, source='CREDIT_CARD')
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Purchase amount must be greater than 0")

        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM credit_cards WHERE id = ?", (card_id,))
        card = cur.fetchone()
        if not card:
            raise ValueError(f"Credit card not found: {card_id}")

        tx_id = self._generate_id("tx")
        now_str = datetime.now(timezone.utc).isoformat()
        if not tx_date:
            tx_date = date.today().isoformat()

        new_card_bal = float(card["current_balance"]) + amount
        card_acc_id = card["account_id"] or card_id

        with conn:
            # 1. Update credit card balance
            conn.execute(
                "UPDATE credit_cards SET current_balance = ?, updated_at = ? WHERE id = ?",
                (new_card_bal, now_str, card_id)
            )

            # 2. Insert transaction (direction='EXPENSE', note includes card info, cash account not touched)
            conn.execute(
                """INSERT INTO transactions 
                   (id, date, account_id, category_id, subcategory_id, amount, direction, note, source, status, created_at, updated_at) 
                   VALUES (?, ?, ?, ?, ?, ?, 'EXPENSE', ?, 'CREDIT_CARD', 'ACTIVE', ?, ?)""",
                (tx_id, tx_date, card_acc_id, category_id, subcategory_id, amount, note or f"CC Purchase: {card['name']}", now_str, now_str)
            )

            if subcategory_id:
                self.record_transaction_metadata(tx_id, subcategory_id=subcategory_id)

            # 3. Audit log
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "credit_cards", card_id, "PURCHASE", now_str)
            )

        return {
            "success": True,
            "transaction_id": tx_id,
            "card_id": card_id,
            "amount": amount,
            "new_card_balance": new_card_bal
        }

    def advance_mortgage_payment(
        self,
        liability_id: str,
        payment_number: Optional[int] = None,
        amount: float = 0.0,
        principal_portion: float = 0.0,
        interest_portion: float = 0.0,
        payment_date: Optional[str] = None,
        notes: Optional[str] = None,
        account_id: Optional[str] = None
    ) -> LiabilityPayment:
        """
        Advances mortgage schedule (e.g. Cicilan #58/120):
        - Cash account is deducted by total payment if account_id is provided
        - If split missing: principal_interest_pending=true, full payment is NEVER classified as expense
        - If split available: interest is expense, principal reduces mortgage liability
        - Updates remaining balance on liability
        """
        if payment_number is None:
            existing = self.list_liability_payments(liability_id)
            payment_number = len(existing) + 1
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Mortgage payment amount must be positive")

        if not payment_date:
            payment_date = date.today().isoformat()

        conn = self.db.get_connection()
        cur_liab = conn.execute("SELECT * FROM liabilities WHERE id = ?", (liability_id,)).fetchone()
        if not cur_liab:
            raise ValueError(f"Liability not found: {liability_id}")

        principal_interest_pending = (principal_portion == 0.0 and interest_portion == 0.0)
        p_note = notes or ""
        if principal_interest_pending:
            p_note = f"Cicilan #{payment_number}/120 (principal_interest_pending=true)" if not p_note else f"Cicilan #{payment_number}/120: {p_note} (principal_interest_pending=true)"
        else:
            p_note = f"Cicilan #{payment_number}/120: {p_note}".strip(": ")

        now_str = datetime.now(timezone.utc).isoformat()
        tx_id = None

        with conn:
            # 1. Deduct cash account if provided
            if account_id:
                cur_acc = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
                if not cur_acc:
                    raise ValueError(f"Cash account not found: {account_id}")
                new_bal = float(cur_acc["balance"]) - amount
                conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_bal, account_id))

                # 2. Insert cash movement transaction
                if interest_portion > 0:
                    int_tx_id = self._generate_id("tx")
                    conn.execute(
                        """INSERT INTO transactions 
                           (id, date, account_id, category_id, amount, direction, note, source, status, created_at, updated_at) 
                           VALUES (?, ?, ?, NULL, ?, 'EXPENSE', ?, 'MORTGAGE_PAYMENT', 'ACTIVE', ?, ?)""",
                        (int_tx_id, payment_date, account_id, float(interest_portion), f"Bunga {p_note}", now_str, now_str)
                    )
                    if principal_portion > 0:
                        princ_tx_id = self._generate_id("tx")
                        conn.execute(
                            """INSERT INTO transactions 
                               (id, date, account_id, category_id, amount, direction, note, source, status, created_at, updated_at) 
                               VALUES (?, ?, ?, NULL, ?, 'TRANSFER', ?, 'MORTGAGE_PAYMENT', 'ACTIVE', ?, ?)""",
                            (princ_tx_id, payment_date, account_id, float(principal_portion), f"Pokok {p_note}", now_str, now_str)
                        )
                    tx_id = int_tx_id
                else:
                    gen_tx_id = self._generate_id("tx")
                    conn.execute(
                        """INSERT INTO transactions 
                           (id, date, account_id, category_id, amount, direction, note, source, status, created_at, updated_at) 
                           VALUES (?, ?, ?, NULL, ?, 'TRANSFER', ?, 'MORTGAGE_PAYMENT', 'ACTIVE', ?, ?)""",
                        (gen_tx_id, payment_date, account_id, amount, p_note, now_str, now_str)
                    )
                    tx_id = gen_tx_id

        return self.record_liability_payment(
            liability_id=liability_id,
            payment_date=payment_date,
            amount=amount,
            principal_portion=principal_portion,
            interest_portion=interest_portion,
            transaction_id=tx_id,
            notes=p_note
        )

    def get_mortgage_summary(self, liability_id: str) -> Dict[str, Any]:
        liab = self.get_liability(liability_id)
        if not liab:
            raise ValueError(f"Liability not found: {liability_id}")
        payments = self.list_liability_payments(liability_id)
        paid_count = len(payments)
        next_installment = paid_count + 1
        return {
            "liability_id": liab.id,
            "name": liab.name,
            "start_date": "2022-01",
            "tenor_months": 120,
            "paid_installments": paid_count,
            "next_installment": next_installment,
            "original_amount": liab.original_amount,
            "remaining_amount": liab.remaining_amount,
            "monthly_payment": liab.monthly_payment,
            "payment_history_count": len(payments)
        }




