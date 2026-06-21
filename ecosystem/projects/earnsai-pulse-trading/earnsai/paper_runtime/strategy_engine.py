from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Dict, List, Optional


@dataclass
class StrategySignal:
    symbol: str
    action: str
    confidence: float
    reason: List[str]
    price: float
    indicators: Dict[str, Any]


class StrategyEngine:
    """
    Signal-based strategy engine.

    This strategy does not trade based on time.
    The runtime may check the strategy every tick, but execution only happens
    when the strategy returns BUY or SELL with enough confidence.
    """

    def __init__(self, config: Dict[str, Any]):
        strategy = config["strategy"]
        self.symbol = config["symbol"]
        self.short_window = int(strategy["short_window"])
        self.long_window = int(strategy["long_window"])
        self.rsi_period = int(strategy["rsi_period"])
        self.buy_rsi_max = float(strategy["buy_rsi_max"])
        self.sell_rsi_min = float(strategy["sell_rsi_min"])
        self.min_confidence = float(strategy["min_confidence"])
        self.history: List[float] = []
        self.last_fast_above: Optional[bool] = None

    def update_price(self, price: float, max_history: int = 300) -> None:
        self.history.append(float(price))
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]

    def _ma(self, window: int) -> Optional[float]:
        if len(self.history) < window:
            return None
        return mean(self.history[-window:])

    def _rsi(self) -> Optional[float]:
        if len(self.history) <= self.rsi_period:
            return None

        recent = self.history[-(self.rsi_period + 1):]
        gains = []
        losses = []

        for prev, cur in zip(recent, recent[1:]):
            delta = cur - prev
            if delta >= 0:
                gains.append(delta)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(delta))

        avg_gain = mean(gains)
        avg_loss = mean(losses)

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        return 100.0 - (100.0 / (1.0 + rs))

    def generate_signal(self, price: float, portfolio_state: Dict[str, Any]) -> StrategySignal:
        self.update_price(price, int(portfolio_state.get("max_price_history", 300)))

        short_ma = self._ma(self.short_window)
        long_ma = self._ma(self.long_window)
        rsi = self._rsi()

        indicators = {
            "short_ma": short_ma,
            "long_ma": long_ma,
            "rsi": rsi,
            "history_len": len(self.history),
        }

        if short_ma is None or long_ma is None or rsi is None:
            return StrategySignal(
                symbol=self.symbol,
                action="HOLD",
                confidence=0.0,
                reason=["Not enough history for MA/RSI calculation."],
                price=price,
                indicators=indicators,
            )

        fast_above = short_ma > long_ma
        previous_fast_above = self.last_fast_above
        self.last_fast_above = fast_above

        has_position = float(portfolio_state.get("position_qty", 0.0)) > 0

        ma_gap = abs(short_ma - long_ma) / max(long_ma, 1e-9)
        confidence = min(0.95, 0.50 + ma_gap * 100.0)

        reason = [
            f"short_ma={short_ma:.2f}",
            f"long_ma={long_ma:.2f}",
            f"rsi={rsi:.2f}",
            f"ma_gap={ma_gap:.5f}",
        ]

        if previous_fast_above is None:
            return StrategySignal(
                symbol=self.symbol,
                action="HOLD",
                confidence=confidence,
                reason=reason + ["Initial crossover state recorded. Waiting for next confirmed signal."],
                price=price,
                indicators=indicators,
            )

        crossed_up = (not previous_fast_above) and fast_above
        crossed_down = previous_fast_above and (not fast_above)

        if crossed_up and not has_position and rsi <= self.buy_rsi_max and confidence >= self.min_confidence:
            return StrategySignal(
                symbol=self.symbol,
                action="BUY",
                confidence=confidence,
                reason=reason + ["BUY signal: short MA crossed above long MA and RSI is acceptable."],
                price=price,
                indicators=indicators,
            )

        if has_position and (crossed_down or rsi >= self.sell_rsi_min) and confidence >= self.min_confidence:
            sell_reason = "SELL signal: "
            sell_reason += "short MA crossed below long MA." if crossed_down else "RSI reached overbought exit zone."
            return StrategySignal(
                symbol=self.symbol,
                action="SELL",
                confidence=confidence,
                reason=reason + [sell_reason],
                price=price,
                indicators=indicators,
            )

        return StrategySignal(
            symbol=self.symbol,
            action="HOLD",
            confidence=confidence,
            reason=reason + ["No executable signal. Runtime continues monitoring."],
            price=price,
            indicators=indicators,
        )
