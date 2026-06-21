echo "--- [ BOT STATUS ] ---"
ps aux | grep paper_bot.py | grep -v grep || echo "Bot is sleeping (Waiting for Cron)"
echo -e "\n--- [ LAST 5 LOGS ] ---"
tail -n 5 bot_log.log 2>/dev/null || echo "No logs yet."
echo -e "\n--- [ RECENT TRADES ] ---"
tail -n 5 paper_trades.csv 2>/dev/null || echo "No trades yet."
echo -e "\n--- [ PERFORMANCE ] ---"
python3 report.py
