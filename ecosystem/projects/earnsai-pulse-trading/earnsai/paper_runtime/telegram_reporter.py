from __future__ import annotations

import os
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class TelegramReporter:
    def __init__(self) -> None:
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    @property
    def enabled(self) -> bool:
        return bool(self.token and self.chat_id)

    def send(self, text: str) -> bool:
        # Normalize escaped newline sequences so Telegram renders readable multiline reports.
        text = text.replace("\\n", "\n")
        if not self.enabled:
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": "true",
        }).encode()

        with urllib.request.urlopen(url, data=data, timeout=20) as response:
            return response.status == 200

    def format_periodic_report(self, perf: Dict[str, Any], insight: str, latest_trade: Optional[Dict[str, Any]]) -> str:
        trade_text = "Tidak ada trade baru."
        if latest_trade:
            trade_text = (
                f"{latest_trade['side']} {latest_trade['symbol']}\\n"
                f"Price: `{latest_trade['price']}`\\n"
                f"Qty: `{latest_trade['qty']}`\\n"
                f"Realized P/L: `{latest_trade['realized_pnl']}`"
            )

        return (
            "📊 *EarnsAI Pulse Paper Runtime Report*\\n"
            "\\n"
            f"Mode: `PAPER_ONLY`\\n"
            f"Live lock: `true`\\n"
            f"Symbol: `{perf['symbol']}`\\n"
            f"Price: `{perf['price']}`\\n"
            "\\n"
            "💼 *Virtual Portfolio*\\n"
            f"Equity: `${perf['equity']}`\\n"
            f"Cash: `${perf['cash']}`\\n"
            f"Position Qty: `{perf['position_qty']}`\\n"
            f"Realized P/L: `${perf['realized_pnl']}`\\n"
            f"Unrealized P/L: `${perf['unrealized_pnl']}`\\n"
            f"Total P/L: `${perf['total_pnl']}` (`{perf['total_return_pct']}%`)\\n"
            "\\n"
            "📈 *Performance*\\n"
            f"Trades: `{perf['total_trades']}`\\n"
            f"Win rate: `{perf['win_rate_pct']}%`\\n"
            f"Max drawdown: `{perf['max_drawdown_pct']}%`\\n"
            f"Buy & Hold: `{perf['benchmark_buy_hold_return_pct']}%`\\n"
            f"Delta vs benchmark: `{perf['benchmark_delta_pct']}%`\\n"
            "\\n"
            "🧠 *Strategy Insight*\\n"
            f"{insight}\\n"
            "\\n"
            "🧾 *Latest Trade*\\n"
            f"{trade_text}"
        )

    def format_trade_alert(self, trade: Dict[str, Any], perf: Dict[str, Any]) -> str:
        emoji = "🟢" if trade["side"] == "BUY" else "🔴"
        return (
            f"{emoji} *EarnsAI Paper Trade Executed*\\n"
            "\\n"
            f"Side: `{trade['side']}`\\n"
            f"Symbol: `{trade['symbol']}`\\n"
            f"Price: `{trade['price']}`\\n"
            f"Qty: `{trade['qty']}`\\n"
            f"Notional: `${trade['notional']}`\\n"
            f"Fee: `${trade['fee']}`\\n"
            f"Realized P/L: `${trade['realized_pnl']}`\\n"
            "\\n"
            f"Equity now: `${perf['equity']}`\\n"
            f"Total P/L: `${perf['total_pnl']}` (`{perf['total_return_pct']}%`)\\n"
            "\\n"
            "Mode: `PAPER_ONLY`\\n"
            "Live trading: `LOCKED`"
        )
