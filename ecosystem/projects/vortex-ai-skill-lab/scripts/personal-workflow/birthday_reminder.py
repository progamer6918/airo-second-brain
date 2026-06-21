#!/usr/bin/env python3
import csv
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
from urllib.request import urlopen, Request


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = Path(os.getenv("BIRTHDAY_CSV_PATH", BASE_DIR / "ultah.csv"))
TIMEZONE = ZoneInfo("Asia/Jakarta")
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"


def setup_logging():
 logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def parse_birth_date(value):
 if not value:
  return None

 value = value.strip()

 for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
  try:
   return datetime.strptime(value, fmt).date()
  except ValueError:
   continue

 return None


def is_valid_birth_year(year):
 current_year = datetime.now(TIMEZONE).year

 if year >= 2024:
  return False

 if year < 1900:
  return False

 if year > current_year:
  return False

 return True


def calculate_age(birth_date, today):
 if not is_valid_birth_year(birth_date.year):
  return "tahun lahir belum pasti"

 age = today.year - birth_date.year

 if (today.month, today.day) < (birth_date.month, birth_date.day):
  age -= 1

 return f"{age} tahun"


def read_birthdays(csv_path):
 rows = []

 if not csv_path.exists:
  raise FileNotFoundError(f"File CSV tidak ditemukan: {csv_path}")

 with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
  reader = csv.DictReader(file)

  required_columns = {"NAMA DEALER", "NAMA", "TANGGAL LAHIR"}
  missing_columns = required_columns - set(reader.fieldnames or [])

  if missing_columns:
   raise ValueError(f"Kolom CSV kurang: {', '.join(sorted(missing_columns))}")

  for row in reader:
   dealer = (row.get("NAMA DEALER") or "").strip()
   name = (row.get("NAMA") or "").strip()
   birth_date_text = (row.get("TANGGAL LAHIR") or "").strip()

   if not name or name == "-":
    continue

   birth_date = parse_birth_date(birth_date_text)

   if not birth_date:
    logging.warning("Tanggal lahir tidak valid, dilewati: %s | %s | %s", dealer, name, birth_date_text)
    continue

   rows.append({
    "dealer": dealer,
    "name": name,
    "birth_date_text": birth_date_text,
    "birth_date": birth_date,
   })

 return rows


def find_birthdays_today(rows, today):
 matches = []

 for row in rows:
  birth_date = row["birth_date"]

  if birth_date.day == today.day and birth_date.month == today.month:
   matches.append(row)

 return matches


def build_message(birthdays_today, today):
 today_text = today.strftime("%d/%m/%Y")

 message_parts = [
  "🎂 Reminder Ulang Tahun Hari Ini",
  f"Tanggal: {today_text}",
  "",
  "Hari ini ada yang ulang tahun:",
  "",
 ]

 for index, person in enumerate(birthdays_today, start=1):
  age_text = calculate_age(person["birth_date"], today)

  message_parts.extend([
   f"{index}. {person['name']}",
   f" Dealer: {person['dealer']}",
   f" Tanggal lahir: {person['birth_date_text']}",
   f" Usia: {age_text}",
   "",
  ])

 message_parts.append("Jangan lupa follow up / kirim ucapan.")

 return "\n".join(message_parts)


def send_telegram_message(bot_token, chat_id, text):
 url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
 payload = urlencode({
  "chat_id": chat_id,
  "text": text,
 }).encode("utf-8")

 request = Request(url, data=payload, method="POST")

 with urlopen(request, timeout=30) as response:
  response_body = response.read().decode("utf-8")
  logging.info("Telegram response: %s", response_body)


def main():
 setup_logging()

 test_run = os.getenv("BIRTHDAY_REMINDER_TEST_RUN", "").lower() in {"1", "true", "yes"}
 bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
 chat_id = os.getenv("TELEGRAM_CHAT_ID")
 today = datetime.now(TIMEZONE).date()

 logging.info("CSV path: %s", CSV_PATH)
 logging.info("Tanggal hari ini: %s", today.strftime("%d/%m"))

 try:
  rows = read_birthdays(CSV_PATH)
 except (FileNotFoundError, ValueError) as e:
  logging.error("Error membaca data ulang tahun: %s", e)
  return 1

 birthdays_today = find_birthdays_today(rows, today)

 logging.info("Total data terbaca: %s", len(rows))
 logging.info("Jumlah ulang tahun hari ini: %s", len(birthdays_today))

 if not birthdays_today:
  logging.info("Tidak ada ulang tahun hari ini. Tidak ada pesan Telegram yang dikirim.")
  return 0

 final_message = build_message(birthdays_today, today)

 if test_run:
  logging.info("TEST RUN aktif. Pesan tidak dikirim ke Telegram.")
  print(final_message)
  return 0

 if not bot_token or not chat_id:
  logging.error("TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID belum tersedia.")
  print("Pastikan TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID sudah di-set sebagai environment variables.")
  return 1

 try:
  send_telegram_message(bot_token, chat_id, final_message)
  logging.info("Reminder ulang tahun berhasil dikirim ke Telegram.")
 except Exception as e:
  logging.error("Terjadi error saat mengirim pesan Telegram: %s", e)
  return 1


if __name__ == "__main__":
 sys.exit(main())