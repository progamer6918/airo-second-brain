import telebot
import ccxt
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# ==============================
# EARNSAI PULSE TRADING BOT v3.1
# Phase 4 — Trading Research Lab
# ==============================

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan. Cek file .env")

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.bybit()

DATA_FILE = "trading_data.json"
DEFAULT_DATA = {
    "balance_usdt": 50000.0,
    "balance_btc": 0.0,
    "entry_price": 0.0
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)

            for key, value in DEFAULT_DATA.items():
                if key not in data:
                    data[key] = value

            return data
        except json.JSONDecodeError:
            print("⚠️ trading_data.json rusak. Menggunakan default data sementara.")
            return DEFAULT_DATA.copy()

    return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_btc_price():
    """
    Lightweight Bybit public ticker fetch.
    Avoids CCXT market-loading endpoint that may fail on instruments-info.
    """
    import requests

    url = "https://api.bybit.com/v5/market/tickers"
    params = {
        "category": "spot",
        "symbol": "BTCUSDT"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    payload = response.json()
    result = payload.get("result", {})
    items = result.get("list", [])

    if not items:
        raise RuntimeError("Bybit ticker response kosong")

    return float(items[0]["lastPrice"])


def format_money(value):
    return f"${value:,.2f}"


user_data = load_data()

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 EARNSAI PULSE v3.1 - PHASE 4 READY")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    resp = (
        "🤖 *EARNSAI PULSE v3.1*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Phase 4 — Trading Research Lab\n\n"
        "*Command tersedia:*\n"
        "/price - Cek harga BTC real-time\n"
        "/buy - Simulasi beli BTC senilai 1000 USDT\n"
        "/sell - Simulasi jual semua BTC\n"
        "/balance - Cek portfolio & unrealized P/L\n"
        "/status - Cek status sistem bot\n\n"
        "Mode: Virtual trading only, bukan live trading real money."
    )
    bot.reply_to(message, resp, parse_mode="Markdown")


@bot.message_handler(commands=["price"])
def price_command(message):
    try:
        price = get_btc_price()
        resp = (
            "📈 *BTC/USDT PRICE*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Bybit Last Price: {format_money(price)}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal ambil harga BTC: {e}")


@bot.message_handler(commands=["buy"])
def buy_command(message):
    global user_data

    try:
        price = get_btc_price()
        spent = 1000.0

        if user_data["balance_usdt"] < spent:
            bot.reply_to(message, "❌ Balance USDT tidak cukup untuk BUY 1000 USDT.")
            return

        qty = spent / price

        old_btc = user_data["balance_btc"]
        old_entry = user_data["entry_price"]

        if old_btc > 0:
            new_entry = ((old_btc * old_entry) + (qty * price)) / (old_btc + qty)
        else:
            new_entry = price

        user_data["balance_usdt"] -= spent
        user_data["balance_btc"] += qty
        user_data["entry_price"] = new_entry

        save_data(user_data)

        resp = (
            "🎯 *BUY EXECUTED — VIRTUAL*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Spent: {format_money(spent)}\n"
            f"Price: {format_money(price)}\n"
            f"BTC Bought: {qty:.8f}\n"
            f"BTC Total: {user_data['balance_btc']:.8f}\n"
            f"Average Entry: {format_money(user_data['entry_price'])}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error saat BUY: {e}")


@bot.message_handler(commands=["sell"])
def sell_command(message):
    global user_data

    try:
        price = get_btc_price()

        if user_data["balance_btc"] <= 0:
            bot.reply_to(message, "❌ Tidak ada BTC untuk dijual.")
            return

        btc_qty = user_data["balance_btc"]
        entry_price = user_data["entry_price"]

        received = btc_qty * price
        cost_basis = btc_qty * entry_price

        pnl = received - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0.0

        user_data["balance_usdt"] += received
        user_data["balance_btc"] = 0.0
        user_data["entry_price"] = 0.0

        save_data(user_data)

        status = "📈 PROFIT" if pnl >= 0 else "📉 LOSS"

        resp = (
            "💰 *SELL EXECUTED — VIRTUAL*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Sold BTC: {btc_qty:.8f}\n"
            f"Sell Price: {format_money(price)}\n"
            f"Received: {format_money(received)}\n"
            f"{status}: {format_money(abs(pnl))} ({pnl_pct:.2f}%)\n"
            f"USDT Balance: {format_money(user_data['balance_usdt'])}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error saat SELL: {e}")


@bot.message_handler(commands=["balance"])
def balance_command(message):
    try:
        price = get_btc_price()

        btc_qty = user_data["balance_btc"]
        btc_value = btc_qty * price

        pnl_live = 0.0
        pnl_pct = 0.0

        if btc_qty > 0 and user_data["entry_price"] > 0:
            cost_basis = btc_qty * user_data["entry_price"]
            pnl_live = btc_value - cost_basis
            pnl_pct = (pnl_live / cost_basis) * 100

        net_worth = user_data["balance_usdt"] + btc_value
        pnl_status = "📈" if pnl_live >= 0 else "📉"

        resp = (
            "💰 *EARNSAI PULSE PORTFOLIO*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 USDT: {format_money(user_data['balance_usdt'])}\n"
            f"₿ BTC: {btc_qty:.8f}\n"
            f"📍 Entry Avg: {format_money(user_data['entry_price'])}\n"
            f"📈 BTC Price: {format_money(price)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"{pnl_status} Unrealized P/L: {format_money(pnl_live)} ({pnl_pct:.2f}%)\n"
            f"💎 Net Worth: {format_money(net_worth)}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error saat BALANCE: {e}")


@bot.message_handler(commands=["status", "system"])
def status_command(message):
    try:
        price = get_btc_price()
        data_exists = os.path.exists(DATA_FILE)
        last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        resp = (
            "🧠 *EARNSAI SYSTEM STATUS*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Bot Version: v3.1\n"
            "Phase: 4 — Trading Research Lab\n"
            "Mode: Virtual Trading Only\n"
            "Exchange: Bybit via CCXT Public\n"
            f"Data File: {'OK' if data_exists else 'MISSING'}\n"
            f"BTC Feed: OK — {format_money(price)}\n"
            f"Last Check: {last_check}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Milestone: v3.0 Persistent Memory LIVE & STABLE"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ System check error: {e}")


@bot.message_handler(func=lambda message: True)
def fallback_message(message):
    resp = (
        "⚠️ Command belum dikenali.\n\n"
        "Gunakan:\n"
        "/price\n"
        "/buy\n"
        "/sell\n"
        "/balance\n"
        "/status\n"
        "/help"
    )
    bot.reply_to(message, resp)


bot.infinity_polling()
