import os
import requests
from dotenv import load_dotenv

# Load secret dari file .env
load_dotenv(dotenv_path="paper-trading/.env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    if not TOKEN or not CHAT_ID or TOKEN == "masukkan_token_bot_di_sini":
        print("❌ ERROR: TOKEN atau CHAT_ID belum diisi di file paper-trading/.env")
        return False
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Pesan berhasil dikirim ke Telegram!")
            return True
        else:
            print(f"❌ Gagal mengirim pesan: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
        return False

if __name__ == "__main__":
    send_telegram_alert("🤖 *EarnsAI Trading Lab*\nTes notifikasi dari server berhasil! Sistem paper trading mulai aktif.")
