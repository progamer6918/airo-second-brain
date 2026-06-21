import yfinance as yf
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("Mengambil data live BTC-USD...")
# Menggunakan yf.download yang lebih robust
df = yf.download("BTC-USD", period="120d", interval="1d", progress=False)

if df.empty:
    print("Gagal mengambil data. Mungkin IP server terkena rate-limit Yahoo Finance.")
    exit()

# Ratakan MultiIndex jika yfinance versi baru mengembalikannya
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Kalkulasi Indikator
df['MA_Fast'] = df['Close'].rolling(window=20).mean()
df['MA_Slow'] = df['Close'].rolling(window=100).mean()

today = df.iloc[-1]
yesterday = df.iloc[-2]

print("=== LIVE MARKET CHECK ===")
print(f"Date    : {today.name.strftime('%Y-%m-%d')}")
print(f"Close   : ${float(today['Close']):,.2f}")
print(f"MA_20   : ${float(today['MA_Fast']):,.2f}")
print(f"MA_100  : ${float(today['MA_Slow']):,.2f}")

# Gunakan float() untuk mencegah error tipe data
if float(yesterday['MA_Fast']) <= float(yesterday['MA_Slow']) and float(today['MA_Fast']) > float(today['MA_Slow']):
    print("SIGNAL  : 🟢 BUY (Golden Cross!)")
elif float(yesterday['MA_Fast']) >= float(yesterday['MA_Slow']) and float(today['MA_Fast']) < float(today['MA_Slow']):
    print("SIGNAL  : 🔴 SELL (Death Cross!)")
else:
    if float(today['MA_Fast']) > float(today['MA_Slow']):
        print("SIGNAL  : ⏳ HOLD (Uptrend - Sedang Naik)")
    else:
        print("SIGNAL  : ⏳ WAIT (Downtrend - Sedang Turun)")
print("=========================")
