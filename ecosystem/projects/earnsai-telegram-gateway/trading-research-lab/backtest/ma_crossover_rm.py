import pandas as pd

df = pd.read_csv('data/BTC-USD_daily.csv', skiprows=3, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], index_col=0, parse_dates=True)
df = df.sort_index()

MA_FAST, MA_SLOW = 20, 100
STOP_LOSS, TAKE_PROFIT = 0.10, 0.15

df['MA_Fast'] = df['Close'].rolling(window=MA_FAST).mean()
df['MA_Slow'] = df['Close'].rolling(window=MA_SLOW).mean()

capital = 10000.0
in_position = False
entry_price = 0.0
trades, wins = 0, 0
equity_curve = []

for date, row in df.dropna().iterrows():
    price = row['Close']
    if in_position:
        if price <= entry_price * (1 - STOP_LOSS):
            capital *= (1 - STOP_LOSS)
            in_position = False
            trades += 1
        elif price >= entry_price * (1 + TAKE_PROFIT):
            capital *= (1 + TAKE_PROFIT)
            in_position = False
            trades += 1
            wins += 1
        elif row['MA_Fast'] < row['MA_Slow']:
            return_pct = (price - entry_price) / entry_price
            capital *= (1 + return_pct)
            in_position = False
            trades += 1
            if return_pct > 0: wins += 1
    else:
        if row['MA_Fast'] > row['MA_Slow']:
            in_position = True
            entry_price = price
    
    equity_curve.append(capital)

df_result = df.dropna().copy()
df_result['Equity'] = equity_curve
df_result[['Equity']].to_csv('backtest/equity_curve_rm.csv')

print(f"Total Return : {((capital - 10000) / 10000) * 100:.2f}% | Trades: {trades}")
