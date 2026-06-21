import pandas as pd
import matplotlib.pyplot as plt

# Baca data equity
df = pd.read_csv('backtest/equity_curve.csv', index_col=0, parse_dates=True)

# Buat grafik
plt.figure(figsize=(10, 5))
plt.plot(df.index, df.iloc[:, 0], label='Portfolio Equity', color='blue', linewidth=1.5)
plt.title('MA Crossover - Equity Curve (BTC-USD)')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Simpan sebagai gambar
plt.savefig('backtest/equity_chart.png', dpi=300)
print("=== CHART_SAVED: backtest/equity_chart.png ===")
