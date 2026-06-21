import telebot
import ccxt
import os
import json
from dotenv import load_dotenv

# 1. Setup & Load Data
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.bybit()
DATA_FILE = 'trading_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"balance_usdt": 50000.0, "balance_btc": 0.0, "entry_price": 0.0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Inisialisasi Data dari "Database"
user_data = load_data()

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 EARNSAI PULSE v3.0 - DATABASE READY")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global user_data
    msg_text = message.text.upper()
    
    # --- FITUR BUY ---
    if "BUY BTC" in msg_text:
        try:
            price = exchange.fetch_ticker('BTC/USDT')['last']
            spent = 1000.0
            if user_data["balance_usdt"] >= spent:
                qty = spent / price
                # Update Average Entry
                if user_data["balance_btc"] > 0:
                    user_data["entry_price"] = ((user_data["balance_btc"] * user_data["entry_price"]) + (qty * price)) / (user_data["balance_btc"] + qty)
                else:
                    user_data["entry_price"] = price
                
                user_data["balance_usdt"] -= spent
                user_data["balance_btc"] += qty
                save_data(user_data) # SIMPAN KE DATABASE
                
                resp = f"🎯 *BUY EXECUTED*\nPrice: ${price:,.2f}\nEntry Avg: ${user_data['entry_price']:,.2f}"
                bot.reply_to(message, resp, parse_mode='Markdown')
            else:
                bot.reply_to(message, "❌ Balance USDT tipis!")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {e}")

    # --- FITUR SELL ---
    elif "SELL BTC" in msg_text:
        try:
            price = exchange.fetch_ticker('BTC/USDT')['last']
            if user_data["balance_btc"] > 0:
                received = user_data["balance_btc"] * price
                pnl = received - (user_data["balance_btc"] * user_data["entry_price"])
                pnl_pct = (pnl / (user_data["balance_btc"] * user_data["entry_price"])) * 100
                
                user_data["balance_usdt"] += received
                user_data["balance_btc"] = 0.0
                user_data["entry_price"] = 0.0
                save_data(user_data) # SIMPAN KE DATABASE
                
                status = "📈 PROFIT" if pnl > 0 else "📉 LOSS"
                resp = f"💰 *SELL EXECUTED*\nPrice: ${price:,.2f}\n{status}: ${abs(pnl):,.2f} ({pnl_pct:.2f}%)"
                bot.reply_to(message, resp, parse_mode='Markdown')
            else:
                bot.reply_to(message, "❌ Gak ada BTC buat dijual.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {e}")

    # --- FITUR BALANCE ---
    elif "BALANCE" in msg_text:
        try:
            price = exchange.fetch_ticker('BTC/USDT')['last']
            current_val = user_data["balance_btc"] * price
            pnl_live = 0.0
            pnl_pct = 0.0
            if user_data["balance_btc"] > 0:
                pnl_live = current_val - (user_data["balance_btc"] * user_data["entry_price"])
                pnl_pct = (pnl_live / (user_data["balance_btc"] * user_data["entry_price"])) * 100

            resp = (
                f"💰 *EARNSAI PULSE PORTFOLIO*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💵 USDT: ${user_data['balance_usdt']:,.2f}\n"
                f"₿ BTC: {user_data['balance_btc']:.6f}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 Unrealized P/L: {pnl_live:,.2f} ({pnl_pct:.2f}%)\n"
                f"💎 Net Worth: ${(user_data['balance_usdt'] + current_val):,.2f}"
            )
            bot.reply_to(message, resp, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {e}")

bot.infinity_polling()
