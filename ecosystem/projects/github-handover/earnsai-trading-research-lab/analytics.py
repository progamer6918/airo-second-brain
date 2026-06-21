import pandas as pd
import os

def run_analytics():
    if not os.path.exists('paper_trades.csv'):
        print("❌ Belum ada data transaksi.")
        return

    df = pd.read_csv('paper_trades.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    summary = []
    
    for symbol in df['Symbol'].unique():
        s_df = df[df['Symbol'] == symbol].sort_values('Timestamp')
        
        trades = 0
        profit = 0
        wins = 0
        buy_p = None
        
        for _, row in s_df.iterrows():
            price = float(row['Price'])
            if row['Action'] == 'BUY':
                buy_p = price
            elif row['Action'] == 'SELL' and buy_p:
                diff = price - buy_p
                profit += diff
                trades += 1
                if diff > 0: wins += 1
                buy_p = None
        
        win_rate = (wins / trades * 100) if trades > 0 else 0
        summary.append({
            'Symbol': symbol,
            'Total Trades': trades,
            'Net Profit ($)': round(profit, 2),
            'Win Rate (%)': f"{win_rate:.1f}%"
        })

    print("\n📊 --- EARNSAI ADVANCED ANALYTICS ---")
    result_df = pd.DataFrame(summary)
    print(result_df.to_string(index=False))
    
    total_net = result_df['Net Profit ($)'].sum()
    print("-" * 40)
    print(f"OVERALL NET PROFIT: ${total_net:,.2f}")
    print("======================================\n")

if __name__ == "__main__":
    run_analytics()
