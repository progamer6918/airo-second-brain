from __future__ import annotations

import argparse
import json
import math
import random
import signal
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from earnsai.paper_runtime.dry_run_executor import DryRunExecutor
from earnsai.paper_runtime.performance_analyzer import PerformanceAnalyzer
from earnsai.paper_runtime.strategy_engine import StrategyEngine
from earnsai.paper_runtime.telegram_reporter import TelegramReporter


STOP_REQUESTED = False


def _handle_stop(signum, frame):
    global STOP_REQUESTED
    STOP_REQUESTED = True


def load_config(path: str) -> Dict[str, Any]:
    config = json.loads(Path(path).read_text(encoding="utf-8"))

    if config.get("mode") != "PAPER_ONLY":
        raise ValueError("Runtime requires mode=PAPER_ONLY")
    if config.get("live_trading_locked") is not True:
        raise ValueError("Runtime requires live_trading_locked=true")

    return config


class SimulatedMarket:
    """
    Lightweight local market simulator.

    It creates moving prices without using private exchange APIs.
    This is intentionally fake market data for paper-only validation.
    """

    def __init__(self, config: Dict[str, Any]):
        sim = config["market_simulation"]
        self.price = float(sim["start_price"])
        self.trend = float(sim["trend_per_tick"])
        self.wave = float(sim["wave_strength"])
        self.noise = float(sim["noise_strength"])
        self.tick_index = 0
        random.seed(42)

    def next_price(self) -> float:
        self.tick_index += 1
        wave_move = math.sin(self.tick_index / 8.0) * self.wave
        noise_move = random.uniform(-self.noise, self.noise)
        pct_move = self.trend + wave_move + noise_move
        self.price = max(1.0, self.price * (1.0 + pct_move))
        return round(self.price, 8)


def build_insight(signal_action: str, signal_reason, perf: Dict[str, Any]) -> str:
    base = "Signal engine aktif. "
    if signal_action == "BUY":
        base += "Strategi melihat momentum masuk yang cukup kuat untuk membuka posisi virtual."
    elif signal_action == "SELL":
        base += "Strategi melihat kondisi exit sehingga posisi virtual ditutup."
    else:
        base += "Belum ada sinyal eksekusi. Runtime hanya monitoring dan tidak memaksa trade."

    base += (
        f" Total P/L `{perf['total_pnl']}` atau `{perf['total_return_pct']}%`, "
        f"drawdown `{perf['max_drawdown_pct']}%`, delta vs buy-hold `{perf['benchmark_delta_pct']}%`."
    )

    if signal_reason:
        base += " Reason terakhir: " + " | ".join(signal_reason[-2:])

    return base


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="runtime/paper_runtime/config.json")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--max-cycles", type=int, default=0)
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _handle_stop)
    signal.signal(signal.SIGTERM, _handle_stop)

    config = load_config(args.config)

    log_path = Path(config["storage"]["runtime_log"])
    log_path.parent.mkdir(parents=True, exist_ok=True)

    market = SimulatedMarket(config)
    strategy = StrategyEngine(config)
    executor = DryRunExecutor(config)
    analyzer = PerformanceAnalyzer(config)
    telegram = TelegramReporter()

    tick_interval = int(config["tick_interval_seconds"])
    report_interval = int(config["report_interval_seconds"])
    max_history = int(config["max_price_history"])

    last_report_ts = 0.0
    cycles = 0

    print("PAPER_RUNTIME_STARTED mode=PAPER_ONLY live_trading_locked=true")
    print(f"telegram_enabled={telegram.enabled}")
    print(f"symbol={config['symbol']} tick_interval_seconds={tick_interval} report_interval_seconds={report_interval}")

    while not STOP_REQUESTED:
        cycles += 1
        price = market.next_price()

        portfolio_context = dict(executor.state)
        portfolio_context["max_price_history"] = max_history

        signal_obj = strategy.generate_signal(price, portfolio_context)
        trade = executor.execute(signal_obj)
        perf = analyzer.snapshot(executor.state, price)
        insight = build_insight(signal_obj.action, signal_obj.reason, perf)

        log_row = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "price": price,
            "action": signal_obj.action,
            "confidence": signal_obj.confidence,
            "trade_executed": bool(trade),
            "equity": perf["equity"],
            "total_pnl": perf["total_pnl"],
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
        }

        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_row) + "\n")

        print(
            f"TICK cycle={cycles} price={price} action={signal_obj.action} "
            f"confidence={signal_obj.confidence:.3f} trade={bool(trade)} "
            f"equity={perf['equity']} pnl={perf['total_pnl']}"
        )

        now = time.time()

        if trade and config.get("trade_notifications", True):
            message = telegram.format_trade_alert(trade, perf)
            try:
                sent = telegram.send(message)
                print("TELEGRAM_TRADE_ALERT_SENT" if sent else "TELEGRAM_TRADE_ALERT_SKIPPED telegram_disabled=true")
            except Exception as exc:
                print(f"TELEGRAM_TRADE_ALERT_FAIL {type(exc).__name__}: {exc}")

        should_report = (now - last_report_ts) >= report_interval
        if config.get("periodic_reports", True) and should_report:
            message = telegram.format_periodic_report(perf, insight, executor.state.get("last_trade"))
            try:
                sent = telegram.send(message)
                print("TELEGRAM_PERIODIC_REPORT_SENT" if sent else "TELEGRAM_PERIODIC_REPORT_SKIPPED telegram_disabled=true")
            except Exception as exc:
                print(f"TELEGRAM_PERIODIC_REPORT_FAIL {type(exc).__name__}: {exc}")
            last_report_ts = now

        if args.once:
            break

        if args.max_cycles and cycles >= args.max_cycles:
            break

        time.sleep(tick_interval)

    print("PAPER_RUNTIME_STOPPED gracefully=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
