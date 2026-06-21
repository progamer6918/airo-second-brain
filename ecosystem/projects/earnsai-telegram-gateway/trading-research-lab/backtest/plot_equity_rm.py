import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('backtest/equity_curve_rm.csv', index_col=0, parse_dates=True)
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Equity'], label='Equity (Risk Management)', color='green', linewidth=1.5)
plt.title('MA Crossover + RM - Equity Curve (BTC-USD)')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

plt.savefig('backtest/equity_chart_rm.png', dpi=300)
print("=== CHART_SAVED: backtest/equity_chart_rm.png ===")
