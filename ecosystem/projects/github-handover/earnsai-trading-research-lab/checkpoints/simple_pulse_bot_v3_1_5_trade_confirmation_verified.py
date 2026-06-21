import telebot
import ccxt
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# ==============================
# EARNSAI PULSE TRADING BOT v3.1.2
# Phase 4 — Trading Research Lab
# ==============================

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan. Cek file .env")

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.bybit()

DATA_FILE = "trading_data.json"
BOT_VERSION = "v3.1.5"
LIVE_PRICE_TIMEOUT = 2
CACHE_MAX_AGE_SECONDS = 60
ADMIN_ID_RAW = os.getenv("TELEGRAM_ADMIN_ID")
ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW and ADMIN_ID_RAW.isdigit() else None
TRADE_CONFIRMATION_TTL_SECONDS = 60

DEFAULT_DATA = {
    "balance_usdt": 50000.0,
    "balance_btc": 0.0,
    "entry_price": 0.0,
    "last_price": 0.0,
    "last_price_source": "none",
    "last_price_updated": 0,
    "last_feed_error": ""
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


def format_money(value):
    return f"${value:,.2f}"


def cache_age_seconds():
    updated = float(user_data.get("last_price_updated") or 0)
    if updated <= 0:
        return None
    return int(time.time() - updated)


def has_valid_cache():
    return float(user_data.get("last_price") or 0) > 0


def get_cached_price():
    cached_price = float(user_data.get("last_price") or user_data.get("entry_price") or 0)
    if cached_price <= 0:
        raise RuntimeError("Belum ada cached price yang valid.")
    user_data["last_price_source"] = "cache"
    save_data(user_data)
    return cached_price



def get_user_id(message):
    return message.from_user.id if message and message.from_user else None


def is_admin(message):
    if ADMIN_ID is None:
        return True
    return get_user_id(message) == ADMIN_ID


def require_trade_permission(message):
    if is_admin(message):
        return True

    bot.reply_to(
        message,
        "🛡 Trade command ditolak.\n"
        "Akun ini bukan TELEGRAM_ADMIN_ID yang diizinkan untuk /buy atau /sell."
    )
    return False


def request_trade_confirmation(message, action):
    user_id = get_user_id(message)
    if not user_id:
        bot.reply_to(message, "⚠️ Tidak bisa membaca Telegram user ID.")
        return

    PENDING_TRADES[user_id] = {
        "action": action,
        "created_at": int(time.time())
    }

    confirm_cmd = "/buy_confirm" if action == "buy" else "/sell_confirm"
    cancel_cmd = "/cancel_trade"

    bot.reply_to(
        message,
        "🛡 *TRADE CONFIRMATION REQUIRED*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"Action: {action.upper()} — VIRTUAL\n"
        f"Expires: {TRADE_CONFIRMATION_TTL_SECONDS} seconds\n\n"
        f"Kirim `{confirm_cmd}` untuk eksekusi.\n"
        f"Kirim `{cancel_cmd}` untuk batal.",
        parse_mode="Markdown"
    )


def consume_trade_confirmation(message, action):
    user_id = get_user_id(message)
    pending = PENDING_TRADES.get(user_id)

    if not pending or pending.get("action") != action:
        bot.reply_to(
            message,
            f"⚠️ Tidak ada pending {action.upper()} confirmation.\n"
            f"Kirim /{action} dulu, lalu /{action}_confirm."
        )
        return False

    age = int(time.time()) - int(pending.get("created_at", 0))

    if age > TRADE_CONFIRMATION_TTL_SECONDS:
        PENDING_TRADES.pop(user_id, None)
        bot.reply_to(message, f"⏳ Pending {action.upper()} sudah expired. Kirim /{action} lagi.")
        return False

    PENDING_TRADES.pop(user_id, None)
    return True

def get_btc_price(force_live=False):
    """
    Fast robust BTC price fetcher.

    Behavior:
    - If cache exists and force_live=False, return cache quickly.
    - If force_live=True, try live feeds with short timeout.
    - If all live feeds fail, fallback to cached/entry price.
    """

    import requests

    global user_data

    if not force_live and has_valid_cache():
        return get_cached_price()

    endpoints = [
        {
            "name": "Bybit",
            "url": "https://api.bybit.com/v5/market/tickers",
            "params": {"category": "spot", "symbol": "BTCUSDT"},
            "extract": lambda payload: float(payload["result"]["list"][0]["lastPrice"]),
        },
        {
            "name": "Binance",
            "url": "https://api.binance.com/api/v3/ticker/price",
            "params": {"symbol": "BTCUSDT"},
            "extract": lambda payload: float(payload["price"]),
        },
        {
            "name": "OKX",
            "url": "https://www.okx.com/api/v5/market/ticker",
            "params": {"instId": "BTC-USDT"},
            "extract": lambda payload: float(payload["data"][0]["last"]),
        },
    ]

    errors = []

    for endpoint in endpoints:
        try:
            response = requests.get(
                endpoint["url"],
                params=endpoint["params"],
                timeout=LIVE_PRICE_TIMEOUT
            )
            response.raise_for_status()
            price = endpoint["extract"](response.json())

            user_data["last_price"] = price
            user_data["last_price_source"] = endpoint["name"]
            user_data["last_price_updated"] = int(time.time())
            user_data["last_feed_error"] = ""
            save_data(user_data)

            return price

        except Exception as err:
            errors.append(f"{endpoint['name']}: {err.__class__.__name__}")

    user_data["last_feed_error"] = " | ".join(errors)
    save_data(user_data)

    return get_cached_price()


user_data = load_data()
PENDING_TRADES = {}

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"🚀 EARNSAI PULSE {BOT_VERSION} - PHASE 4 READY")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


@bot.message_handler(
    func=lambda message: bool(message.text)
    and "\n" in message.text
    and any(line.strip().startswith("/") for line in message.text.splitlines())
)
def multi_command_message(message):
    """
    Process safe read-only commands when user sends multiple commands
    in one Telegram bubble.

    Trading commands are intentionally blocked in multi-command mode
    to prevent accidental BUY/SELL execution.
    """

    raw_lines = message.text.splitlines()
    commands = []

    for line in raw_lines:
        cmd = line.strip().split()[0].lower() if line.strip().startswith("/") else ""
        if cmd:
            commands.append(cmd)

    if not commands:
        bot.reply_to(message, "⚠️ Tidak ada command valid yang terdeteksi.")
        return

    if len(commands) > 5:
        bot.reply_to(message, "⚠️ Terlalu banyak command sekaligus. Maksimal 5 command per pesan.")
        return

    bot.reply_to(message, f"🧩 Multi-command mode: memproses {len(commands)} command aman.")

    for cmd in commands:
        if cmd in ["/status", "/system"]:
            status_command(message)
        elif cmd == "/balance":
            balance_command(message)
        elif cmd == "/price":
            price_command(message)
        elif cmd in ["/help", "/start"]:
            start_command(message)
        elif cmd == "/whoami":
            whoami_command(message)
        elif cmd in ["/buy", "/sell", "/buy_confirm", "/sell_confirm"]:
            bot.reply_to(
                message,
                f"🛡 {cmd} diblokir di multi-command mode. Kirim trade command secara terpisah untuk safety."
            )
        else:
            bot.reply_to(message, f"⚠️ Command tidak dikenali: {cmd}")

        time.sleep(0.3)


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    resp = (
        f"🤖 *EARNSAI PULSE {BOT_VERSION}*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Phase 4 — Trading Research Lab\n\n"
        "*Command tersedia:*\n"
        "/price - Cek harga BTC live\n"
        "/buy - Minta konfirmasi beli BTC senilai 1000 USDT\n/buy_confirm - Eksekusi BUY setelah konfirmasi\n"
        "/sell - Minta konfirmasi jual semua BTC\n/sell_confirm - Eksekusi SELL setelah konfirmasi\n/cancel_trade - Batalkan pending trade\n"
        "/balance - Cek portfolio & unrealized P/L\n"
        "/status - Cek status sistem bot\n"
        "/whoami - Cek Telegram user ID\n\n"
        "Mode: Virtual trading only, bukan live trading real money."
    )
    bot.reply_to(message, resp, parse_mode="Markdown")


@bot.message_handler(commands=["whoami"])
def whoami_command(message):
    user = message.from_user
    user_id = get_user_id(message)

    username = f"@{user.username}" if user and user.username else "-"
    first_name = user.first_name if user and user.first_name else "-"

    admin_status = "YES" if is_admin(message) else "NO"
    guard_status = "NOT CONFIGURED" if ADMIN_ID is None else "CONFIGURED"

    resp = (
        "🪪 *TELEGRAM IDENTITY*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"User ID: `{user_id}`\n"
        f"Name: {first_name}\n"
        f"Username: {username}\n"
        f"Admin Guard: {guard_status}\n"
        f"Is Admin: {admin_status}"
    )
    bot.reply_to(message, resp, parse_mode="Markdown")


@bot.message_handler(commands=["price"])
def price_command(message):
    try:
        price = get_btc_price(force_live=True)
        source = user_data.get("last_price_source", "unknown")
        age = cache_age_seconds()

        age_text = f"{age}s ago" if age is not None else "unknown"

        resp = (
            "📈 *BTC/USDT PRICE*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Price: {format_money(price)}\n"
            f"Source: {source}\n"
            f"Updated: {age_text}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal ambil harga BTC: {e}")


@bot.message_handler(commands=["buy"])
def buy_command(message):
    if not require_trade_permission(message):
        return
    request_trade_confirmation(message, "buy")


@bot.message_handler(commands=["sell"])
def sell_command(message):
    if not require_trade_permission(message):
        return
    request_trade_confirmation(message, "sell")


@bot.message_handler(commands=["cancel_trade"])
def cancel_trade_command(message):
    user_id = get_user_id(message)
    if user_id in PENDING_TRADES:
        PENDING_TRADES.pop(user_id, None)
        bot.reply_to(message, "✅ Pending trade confirmation dibatalkan.")
    else:
        bot.reply_to(message, "ℹ️ Tidak ada pending trade confirmation.")


@bot.message_handler(commands=["buy_confirm"])
def buy_confirm_command(message):
    global user_data

    if not require_trade_permission(message):
        return

    if not consume_trade_confirmation(message, "buy"):
        return

    try:
        price = get_btc_price(force_live=True)
        spent = 1000.0
        source = user_data.get("last_price_source", "unknown")

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
            f"Price Source: {source}\n"
            f"BTC Bought: {qty:.8f}\n"
            f"BTC Total: {user_data['balance_btc']:.8f}\n"
            f"Average Entry: {format_money(user_data['entry_price'])}"
        )
        bot.reply_to(message, resp, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error saat BUY: {e}")


@bot.message_handler(commands=["sell_confirm"])
def sell_confirm_command(message):
    global user_data

    if not require_trade_permission(message):
        return

    if not consume_trade_confirmation(message, "sell"):
        return

    try:
        price = get_btc_price(force_live=True)
        source = user_data.get("last_price_source", "unknown")

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
            f"Price Source: {source}\n"
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
        price = get_btc_price(force_live=False)
        source = user_data.get("last_price_source", "unknown")

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
        age = cache_age_seconds()
        age_text = f"{age}s ago" if age is not None else "unknown"

        resp = (
            "💰 *EARNSAI PULSE PORTFOLIO*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 USDT: {format_money(user_data['balance_usdt'])}\n"
            f"₿ BTC: {btc_qty:.8f}\n"
            f"📍 Entry Avg: {format_money(user_data['entry_price'])}\n"
            f"📈 BTC Price: {format_money(price)}\n"
            f"🛰 Price Source: {source} ({age_text})\n"
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
        price = get_btc_price(force_live=False)
        source = user_data.get("last_price_source", "unknown")
        data_exists = os.path.exists(DATA_FILE)
        last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        age = cache_age_seconds()

        if source == "cache":
            feed_status = "CACHE FALLBACK"
        else:
            feed_status = "LIVE"

        age_text = f"{age}s ago" if age is not None else "unknown"
        last_error = user_data.get("last_feed_error") or "-"

        resp = (
            "🧠 *EARNSAI SYSTEM STATUS*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Bot Version: {BOT_VERSION}\n"
            "Phase: 4 — Trading Research Lab\n"
            "Mode: Virtual Trading Only\n"
            "Exchange Mode: Multi-feed public price\n"
            f"Data File: {'OK' if data_exists else 'MISSING'}\n"
            f"Admin Guard: {'CONFIGURED' if ADMIN_ID is not None else 'NOT CONFIGURED'}\n"
            f"BTC Feed: {feed_status} — {source}\n"
            f"BTC Price: {format_money(price)}\n"
            f"Updated: {age_text}\n"
            f"Last Feed Error: {last_error}\n"
            f"Last Check: {last_check}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Milestone: v3.1.5 Trade Confirmation Layer"
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
        "/buy_confirm\n"
        "/sell\n"
        "/sell_confirm\n"
        "/cancel_trade\n"
        "/balance\n"
        "/status\n"
        "/whoami\n"
        "/help"
    )
    bot.reply_to(message, resp)


bot.infinity_polling()
