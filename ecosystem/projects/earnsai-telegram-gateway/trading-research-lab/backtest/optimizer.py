import pandas as pd
import itertools

# 1. Load Data
df = pd.read_csv('data/BTC-USD_daily.csv', skiprows=3, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], index_col=0, parse_dates=True)
df = df.sort_index()

# 2. Definisikan Angka yang Mau Dites
ma_fasts = [5, 10, 20]
ma_slows = [30, 50, 100, 200]
sls = [0.03, 0.05, 0.10]       # Stop Loss 3%, 5%, 10%
tps = [0.05, 0.10, 0.15, 0.20] # Take Profit 5%, 10%, 15%, 20%

best_return = -999.0
best_params = None

combinations = list(itertools.product(ma_fasts, ma_slows, sls, tps))
print(f"Mencoba {len(combinations)} kombinasi parameter... (Tunggu sebentar)")

# 3. Looping Semua Kombinasi
for fast, slow, sl, tp in combinations:
    if fast >= slow: continue # Abaikan jika MA Fast lebih besar dari Slow
    
    df_temp = df.copy()
    df_temp['MA_Fast'] = df_temp['Close'].rolling(window=fast).mean()
    df_temp['MA_Slow'] = df_temp['Close'].rolling(window=slow).mean()
    
    capital = 10000.0
    in_pos = False
    entry_price = 0.0
    
    for date, row in df_temp.dropna().iterrows():
        price = row['Close']
        if in_pos:
            if price <= entry_price * (1 - sl):
                capital *= (1 - sl)
                in_pos = False
            elif price >= entry_price * (1 + tp):
                capital *= (1 + tp)
                in_pos = False
            elif row['MA_Fast'] < row['MA_Slow']:
                capital *= (1 + (price - entry_price) / entry_price)
                in_pos = False
        else:
            if row['MA_Fast'] > row['MA_Slow']:
                in_pos = True
                entry_price = price
                
    total_return = ((capital - 10000) / 10000) * 100
    
    # Catat jika menemukan return yang lebih tinggi
    if total_return > best_return:
        best_return = total_return
        best_params = (fast, slow, sl, tp)

# 4. Tampilkan Sang Juara
print("\n=== HASIL OPTIMASI TERBAIK ===")
print(f"MA_Fast   : {best_params[0]}")
print(f"MA_Slow   : {best_params[1]}")
print(f"Stop Loss : {best_params[2]*100}%")
print(f"Take Prof : {best_params[3]*100}%")
print(f"RETURN    : {best_return:.2f}%")
print("==============================")
