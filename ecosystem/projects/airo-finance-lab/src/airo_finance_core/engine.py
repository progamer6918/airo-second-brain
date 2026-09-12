import uuid
from datetime import datetime, date, timezone
from typing import Optional, List, Dict, Any, Tuple
from .db import DatabaseManager
from .models import Account, Category, Transaction, Budget, AuditLog

class FinanceCoreEngine:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def _generate_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

    def create_account(self, name: str, account_type: str, initial_balance: float = 0.0) -> Account:
        conn = self.db.get_connection()
        account_id = self._generate_id("acc")
        now_str = datetime.now(timezone.utc).isoformat()
        
        with conn:
            conn.execute(
                "INSERT INTO accounts (id, name, type, balance, created_at) VALUES (?, ?, ?, ?, ?)",
                (account_id, name, account_type.upper(), float(initial_balance), now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "accounts", account_id, "CREATE", now_str)
            )
            
        return Account(id=account_id, name=name, type=account_type.upper(), balance=float(initial_balance), created_at=now_str)

    def create_category(self, name: str) -> Category:
        conn = self.db.get_connection()
        cat_id = self._generate_id("cat")
        now_str = datetime.now(timezone.utc).isoformat()
        
        with conn:
            conn.execute(
                "INSERT INTO categories (id, name, created_at) VALUES (?, ?, ?)",
                (cat_id, name, now_str)
            )
            audit_id = self._generate_id("aud")
            conn.execute(
                "INSERT INTO audit_logs (id, entity, entity_id, action, created_at) VALUES (?, ?, ?, ?, ?)",
                (audit_id, "categories", cat_id, "CREATE", now_str)
            )
            
        return Category(id=cat_id, name=name, created_at=now_str)

    def get_account(self, account_id: str) -> Optional[Account]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cur.fetchone()
        if not row:
            return None
        return Account(id=row["id"], name=row["name"], type=row["type"], balance=row["balance"], created_at=row["created_at"])

    def get_account_by_name(self, name: str) -> Optional[Account]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM accounts WHERE LOWER(name) = LOWER(?)", (name.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return Account(id=row["id"], name=row["name"], type=row["type"], balance=row["balance"], created_at=row["created_at"])

    def get_category_by_name(self, name: str) -> Optional[Category]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM categories WHERE LOWER(name) = LOWER(?)", (name.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return Category(id=row["id"], name=row["name"], created_at=row["created_at"])

    def create_transaction(
        self,
        account_id: str,
        amount: float,
        direction: str,
        category_id: Optional[str] = None,
        note: Optional[str] = None,
        source: str = "MANUAL",
        tx_date: Optional[str] = None
    ) -> Transaction:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
            
        direction = direction.upper()
        if direction not in ("EXPENSE", "INCOME", "TRANSFER"):
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
            else: # TRANSFER
                new_balance = acc_row["balance"] - amount
                
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
            
            # 2. Insert transaction
            conn.execute(
                "INSERT INTO transactions "
                "(id, date, account_id, category_id, amount, direction, note, source, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (tx_id, tx_date, account_id, category_id, amount, direction, note, source, now_str)
            )
            
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
            created_at=now_str
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

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        row = cur.fetchone()
        if not row:
            return None
        return Transaction(
            id=row["id"],
            date=row["date"],
            account_id=row["account_id"],
            category_id=row["category_id"],
            amount=row["amount"],
            direction=row["direction"],
            note=row["note"],
            source=row["source"],
            created_at=row["created_at"]
        )

    def list_transactions(self, limit: int = 50) -> List[Transaction]:
        conn = self.db.get_connection()
        cur = conn.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT ?", (limit,))
        return [
            Transaction(
                id=r["id"],
                date=r["date"],
                account_id=r["account_id"],
                category_id=r["category_id"],
                amount=r["amount"],
                direction=r["direction"],
                note=r["note"],
                source=r["source"],
                created_at=r["created_at"]
            )
            for r in cur.fetchall()
        ]

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
