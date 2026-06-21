from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class DryRunExecutor:
    """
    Paper-only executor.

    It simulates orders using virtual cash and virtual position.
    It never sends orders to an exchange.
    """

    def __init__(self, config: Dict[str, Any]):
        if config.get("mode") != "PAPER_ONLY":
            raise ValueError("DryRunExecutor requires mode=PAPER_ONLY")
        if config.get("live_trading_locked") is not True:
            raise ValueError("DryRunExecutor requires live_trading_locked=true")

        self.config = config
        self.state_path = Path(config["storage"]["state_json"])
        self.trades_csv = Path(config["storage"]["trades_csv"])
        self.signals_jsonl = Path(config["storage"]["signals_jsonl"])

        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.trades_csv.parent.mkdir(parents=True, exist_ok=True)
        self.signals_jsonl.parent.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()

    def _default_state(self) -> Dict[str, Any]:
        return {
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
            "cash": float(self.config["initial_cash"]),
            "position_qty": 0.0,
            "avg_entry_price": 0.0,
            "realized_pnl": 0.0,
            "total_fees": 0.0,
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "last_trade": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _load_state(self) -> Dict[str, Any]:
        if not self.state_path.exists():
            state = self._default_state()
            self._save_state(state)
            return state

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        state["mode"] = "PAPER_ONLY"
        state["live_trading_locked"] = True
        return state

    def _save_state(self, state: Dict[str, Any]) -> None:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _append_signal(self, signal: Any) -> None:
        payload = asdict(signal)
        payload.update({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
        })
        with self.signals_jsonl.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

    def _append_trade(self, trade: Dict[str, Any]) -> None:
        exists = self.trades_csv.exists()
        with self.trades_csv.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "created_at",
                "symbol",
                "side",
                "price",
                "qty",
                "notional",
                "fee",
                "realized_pnl",
                "cash_after",
                "position_qty_after",
                "reason",
            ])
            if not exists:
                writer.writeheader()
            writer.writerow(trade)

    def equity(self, price: float) -> float:
        return float(self.state["cash"]) + float(self.state["position_qty"]) * price

    def execute(self, signal: Any) -> Optional[Dict[str, Any]]:
        self._append_signal(signal)

        action = signal.action
        price = float(signal.price)
        fee_rate = float(self.config["fee_rate"])
        slippage_rate = float(self.config["slippage_rate"])

        if action == "HOLD":
            self._save_state(self.state)
            return None

        if action == "BUY":
            if float(self.state["position_qty"]) > 0:
                return None

            equity = self.equity(price)
            budget = equity * float(self.config["position_pct"])
            executable_price = price * (1.0 + slippage_rate)
            qty = budget / executable_price
            notional = qty * executable_price
            fee = notional * fee_rate

            if notional + fee > float(self.state["cash"]):
                return None

            self.state["cash"] = float(self.state["cash"]) - notional - fee
            self.state["position_qty"] = qty
            self.state["avg_entry_price"] = executable_price
            self.state["total_fees"] = float(self.state["total_fees"]) + fee
            self.state["total_trades"] = int(self.state["total_trades"]) + 1

            trade = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "symbol": signal.symbol,
                "side": "BUY",
                "price": round(executable_price, 8),
                "qty": round(qty, 10),
                "notional": round(notional, 8),
                "fee": round(fee, 8),
                "realized_pnl": 0.0,
                "cash_after": round(float(self.state["cash"]), 8),
                "position_qty_after": round(float(self.state["position_qty"]), 10),
                "reason": " | ".join(signal.reason),
            }

            self.state["last_trade"] = trade
            self._append_trade(trade)
            self._save_state(self.state)
            return trade

        if action == "SELL":
            qty = float(self.state["position_qty"])
            if qty <= 0:
                return None

            executable_price = price * (1.0 - slippage_rate)
            notional = qty * executable_price
            fee = notional * fee_rate
            avg_entry = float(self.state["avg_entry_price"])
            realized_pnl = (executable_price - avg_entry) * qty - fee

            self.state["cash"] = float(self.state["cash"]) + notional - fee
            self.state["position_qty"] = 0.0
            self.state["avg_entry_price"] = 0.0
            self.state["realized_pnl"] = float(self.state["realized_pnl"]) + realized_pnl
            self.state["total_fees"] = float(self.state["total_fees"]) + fee
            self.state["total_trades"] = int(self.state["total_trades"]) + 1

            if realized_pnl >= 0:
                self.state["winning_trades"] = int(self.state["winning_trades"]) + 1
            else:
                self.state["losing_trades"] = int(self.state["losing_trades"]) + 1

            trade = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "symbol": signal.symbol,
                "side": "SELL",
                "price": round(executable_price, 8),
                "qty": round(qty, 10),
                "notional": round(notional, 8),
                "fee": round(fee, 8),
                "realized_pnl": round(realized_pnl, 8),
                "cash_after": round(float(self.state["cash"]), 8),
                "position_qty_after": 0.0,
                "reason": " | ".join(signal.reason),
            }

            self.state["last_trade"] = trade
            self._append_trade(trade)
            self._save_state(self.state)
            return trade

        return None
