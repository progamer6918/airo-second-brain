import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import telebot
import sys

# 1. Konfigurasi
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BOT_DISPLAY_NAME = "EarnsAI Multi-Asset Bot"

# Daftar koin yang dipantau
SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD"]
STOP_LOSS_PCT = 0.05   # 5%
TAKE_PROFIT_PCT = 0.10 # 10%

if not BOT_TOKEN or not CHAT_ID:
    print("❌ ERROR: Konfigurasi .env tidak lengkap")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN.strip())

def get_live_data(symbol):
    try:
        df = yf.download(symbol, period="5d", interval="1h", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return pd.DataFrame()

def log_trade(symbol, action, price):
    log_file = "paper_trades.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_log = pd.DataFrame([[now, symbol, action, price]], columns=['Timestamp', 'Symbol', 'Action', 'Price'])
    new_log.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)

def get_open_position(symbol):
    """Cek apakah kita punya posisi BUY yang belum di-SELL untuk koin ini."""
    if not os.path.exists("paper_trades.csv"): return None
    df = pd.read_csv("paper_trades.csv")
    df_symbol = df[df['Symbol'] == symbol]
    if df_symbol.empty: return None
    last_action = df_symbol.iloc[-1]
    return last_action if last_action['Action'] == 'BUY' else None

def apply_strategy(df, symbol):
    if df.empty or len(df) < 20: return "HOLD", 0
    
    close_prices = df['Close']
    current_price = float(close_prices.iloc[-1])
    
    # --- LOGIKA RISK MANAGEMENT (SL/TP) ---
    open_pos = get_open_position(symbol)
    if open_pos is not None:
        buy_price = float(open_pos['Price'])
        change = (current_price - buy_price) / buy_price
        
        if change <= -STOP_LOSS_PCT:
            return "SELL (SL)", current_price
        if change >= TAKE_PROFIT_PCT:
            return "SELL (TP)", current_price

    # --- LOGIKA STRATEGI (RSI + EMA) ---
    ema_20 = close_prices.ewm(span=20, adjust=False).mean()
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss.replace(0, 0.001)
    rsi = 100 - (100 / (1 + rs))
    
    last_rsi = float(rsi.iloc[-1])
    last_ema = float(ema_20.iloc[-1])

    if last_rsi < 35 and current_price > last_ema and open_pos is None:
        return "BUY", current_price
    elif last_rsi > 65 and open_pos is not None:
        return "SELL (RSI)", current_price
    
    return "HOLD", current_price

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Memulai Scanner Multi-Asset...")
    for symbol in SYMBOLS:
        df = get_live_data(symbol)
        if df.empty: continue
        
        signal, price = apply_strategy(df, symbol)
        print(f"• {symbol:<8}: ${price:>10,.2f} | {signal}")

        if "BUY" in signal or "SELL" in signal:
            action_clean = "BUY" if "BUY" in signal else "SELL"
            log_trade(symbol, action_clean, price)
            
            message = (
                f"🤖 **{BOT_DISPLAY_NAME}**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📈 **Asset:** {symbol}\n"
                f"💰 **Price:** ${price:,.2f}\n"
                f"🔔 **Action:** {signal}\n"
                f"📅 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"━━━━━━━━━━━━━━━━━━"
            )
            bot.send_message(CHAT_ID.strip(), message, parse_mode="Markdown")

if __name__ == "__main__":
    main()
