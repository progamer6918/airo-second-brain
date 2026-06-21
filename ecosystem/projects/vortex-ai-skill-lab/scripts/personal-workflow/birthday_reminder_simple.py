#!/usr/bin/env python3
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = Path(os.getenv("BIRTHDAY_CSV_PATH", BASE_DIR / "ultah_sederhana.csv"))
TIMEZONE = ZoneInfo("Asia/Jakarta")


def parse_date(text):
    text = (text or "").strip()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def age_text(birth_date, today):
    if birth_date.year >= 2024 or birth_date.year < 1900:
        return "tahun lahir belum pasti"
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return f"{age} tahun"


def read_rows(csv_path):
    people = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("NAMA") or "").strip()
            birth_text = (row.get("TANGGAL LAHIR") or "").strip()
            if not name or name == "-":
                continue
            birth_date = parse_date(birth_text)
            if birth_date is None:
                print(f"SKIP tanggal tidak valid: {name} | {birth_text}")
                continue
            people.append({"name": name, "birth_text": birth_text, "birth_date": birth_date})
    return people


def build_message(matches, today):
    lines = [
        "🎂 Reminder Ulang Tahun Hari Ini",
        f"Tanggal: {today.strftime('%d/%m/%Y')}",
        "",
        "Hari ini ada yang ulang tahun:",
        "",
    ]

    for i, person in enumerate(matches, 1):
        lines += [
            f"{i}. {person['name']}",
            f"   Tanggal lahir: {person['birth_text']}",
            f"   Usia: {age_text(person['birth_date'], today)}",
            "",
        ]

    lines.append("Jangan lupa follow up / kirim ucapan.")
    return "\n".join(lines)


def send_telegram(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("ERROR: TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID belum tersedia.")
        return 1

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = Request(url, data=data, method="POST")

    with urlopen(req, timeout=30) as resp:
        print(resp.read().decode("utf-8"))

    return 0


def main():
    test_run = os.getenv("BIRTHDAY_REMINDER_TEST_RUN", "").lower() in ("1", "true", "yes")

    override_date = os.getenv("BIRTHDAY_TEST_DATE", "").strip()
    if override_date:
        today = datetime.strptime(override_date, "%d/%m/%Y").date()
    else:
        today = datetime.now(TIMEZONE).date()

    print(f"CSV: {CSV_PATH}")
    print(f"Tanggal cek: {today.strftime('%d/%m/%Y')}")

    if not CSV_PATH.exists():
        print(f"ERROR: CSV tidak ditemukan: {CSV_PATH}")
        return 1

    people = read_rows(CSV_PATH)
    matches = [p for p in people if p["birth_date"].day == today.day and p["birth_date"].month == today.month]

    print(f"Total data terbaca: {len(people)}")
    print(f"Jumlah ultah hari ini: {len(matches)}")

    if not matches:
        print("Tidak ada yang ulang tahun hari ini. Tidak mengirim Telegram.")
        return 0

    message = build_message(matches, today)

    if test_run:
        print("\n--- PESAN TEST, BELUM DIKIRIM KE TELEGRAM ---")
        print(message)
        print("--- END ---")
        return 0

    return send_telegram(message)


if __name__ == "__main__":
    sys.exit(main())