from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class PerformanceAnalyzer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.path = Path(config["storage"]["performance_jsonl"])
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initial_cash = float(config["initial_cash"])
        self.first_price = None

    def _read_rows(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rows.append(json.loads(line))
        return rows

    def _max_drawdown(self, equities: List[float]) -> float:
        peak = None
        max_dd = 0.0
        for equity in equities:
            if peak is None or equity > peak:
                peak = equity
            if peak and peak > 0:
                dd = (peak - equity) / peak
                max_dd = max(max_dd, dd)
        return max_dd

    def snapshot(self, state: Dict[str, Any], price: float) -> Dict[str, Any]:
        if self.first_price is None:
            rows = self._read_rows()
            self.first_price = rows[0]["price"] if rows else price

        cash = float(state.get("cash", self.initial_cash))
        qty = float(state.get("position_qty", 0.0))
        avg_entry = float(state.get("avg_entry_price", 0.0))
        realized = float(state.get("realized_pnl", 0.0))

        position_value = qty * price
        equity = cash + position_value
        unrealized = (price - avg_entry) * qty if qty > 0 else 0.0
        total_return_pct = ((equity - self.initial_cash) / self.initial_cash) * 100.0

        benchmark_equity = self.initial_cash * (price / self.first_price) if self.first_price else self.initial_cash
        benchmark_return_pct = ((benchmark_equity - self.initial_cash) / self.initial_cash) * 100.0

        rows = self._read_rows()
        equities = [float(row["equity"]) for row in rows] + [equity]

        wins = int(state.get("winning_trades", 0))
        losses = int(state.get("losing_trades", 0))
        closed = wins + losses
        win_rate = (wins / closed * 100.0) if closed else 0.0

        snap = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
            "symbol": self.config["symbol"],
            "price": round(price, 8),
            "cash": round(cash, 8),
            "position_qty": round(qty, 10),
            "position_value": round(position_value, 8),
            "equity": round(equity, 8),
            "realized_pnl": round(realized, 8),
            "unrealized_pnl": round(unrealized, 8),
            "total_pnl": round(equity - self.initial_cash, 8),
            "total_return_pct": round(total_return_pct, 4),
            "win_rate_pct": round(win_rate, 2),
            "max_drawdown_pct": round(self._max_drawdown(equities) * 100.0, 4),
            "total_trades": int(state.get("total_trades", 0)),
            "benchmark_buy_hold_return_pct": round(benchmark_return_pct, 4),
            "benchmark_delta_pct": round(total_return_pct - benchmark_return_pct, 4),
        }

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(snap) + "\n")

        return snap

    def latest_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self._read_rows()[-limit:]
