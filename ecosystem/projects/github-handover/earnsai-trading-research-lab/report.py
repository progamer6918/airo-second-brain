import pandas as pd
import os

def generate_report():
    if not os.path.exists('paper_trades.csv'):
        print("❌ Data belum tersedia.")
        return

    df = pd.read_csv('paper_trades.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(['Symbol', 'Timestamp'])

    print(f"\n=== EARNSAI MULTI-ASSET REPORT ===")
    
    for symbol in df['Symbol'].unique():
        symbol_df = df[df['Symbol'] == symbol]
        total_pl, buy_price = 0, None
        
        print(f"\n>> Asset: {symbol}")
        print(f"{'Date':<20} | {'Action':<5} | {'Price':<12} | {'P/L'}")
        print("-" * 55)
        
        for _, row in symbol_df.iterrows():
            price = float(row['Price'])
            if row['Action'] == 'BUY':
                buy_price = price
                print(f"{row['Timestamp'].strftime('%Y-%m-%d %H:%M'):<20} | BUY   | ${price:<11,.2f} | -")
            elif row['Action'] == 'SELL' and buy_price:
                pl = price - buy_price
                total_pl += pl
                print(f"{row['Timestamp'].strftime('%Y-%m-%d %H:%M'):<20} | SELL  | ${price:<11,.2f} | {pl:>+10,.2f}")
                buy_price = None
        
        print(f"Total P/L for {symbol}: ${total_pl:,.2f}")
    print("\n===================================\n")

if __name__ == "__main__":
    generate_report()
