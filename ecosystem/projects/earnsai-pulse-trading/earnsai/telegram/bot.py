from __future__ import annotations

import os

from earnsai.telegram.handlers import handle_command


def dispatch_text(text: str) -> str:
    response = handle_command(text)
    return response.get("message", "No message generated.")


def main() -> int:
    token_present = bool(os.getenv("TELEGRAM_BOT_TOKEN"))
    if token_present:
        print("TELEGRAM_BOT_TOKEN detected, but local smoke does not start network polling.")
    else:
        print("TELEGRAM_BOT_TOKEN not set. Running command router in dry-run mode.")

    for command in ["/help", "/status", "/signal", "/risk", "/journal", "/health", "/metrics", "/report", "/lock_live"]:
        print(f"\n> {command}")
        print(dispatch_text(command))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
