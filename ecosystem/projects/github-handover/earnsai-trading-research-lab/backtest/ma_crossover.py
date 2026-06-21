import pandas as pd

def run_ma_crossover():
    # Fix khusus untuk format yfinance CSV (skip 2 baris header)
    df = pd.read_csv('data/BTC-USD_daily.csv', 
                     skiprows=3, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'],
                     index_col=0, 
                     parse_dates=True)
    df = df.sort_index()

    # Moving Averages
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()

    # Signal: 1 = Long, 0 = Flat
    df['Signal'] = 0
    df.loc[df['SMA50'] > df['SMA200'], 'Signal'] = 1

    # Backtest logic
    df['Position'] = df['Signal'].shift(1).fillna(0)
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'] * df['Return']

    # Equity curve
    df['Equity'] = (1 + df['Strategy_Return']).cumprod()
    df['Peak'] = df['Equity'].cummax()
    df['Drawdown'] = (df['Equity'] - df['Peak']) / df['Peak']

    # Metrics
    total_return = (df['Equity'].iloc[-1] - 1) * 100
    max_dd = df['Drawdown'].min() * 100
    num_trades = (df['Signal'].diff() != 0).sum()
    win_rate = (df['Strategy_Return'] > 0).mean() * 100

    print("\n=== MA CROSSOVER BACKTEST (BTC-USD 2 Tahun) ===")
    print(f"Total Return     : {total_return:.2f}%")
    print(f"Max Drawdown     : {max_dd:.2f}%")
    print(f"Number of Trades : {num_trades}")
    print(f"Win Rate         : {win_rate:.2f}%")
    print(f"Period           : {df.index[0].date()} → {df.index[-1].date()}")

    # Save equity curve
    df[['Equity']].to_csv('backtest/equity_curve.csv')
    print("\n✅ Equity curve saved → backtest/equity_curve.csv")

if __name__ == "__main__":
    run_ma_crossover()
