from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    checks = {
        "root": ROOT.exists(),
        ".env.example": (ROOT / ".env.example").exists(),
        "Makefile": (ROOT / "Makefile").exists(),
        "signal_schema": (ROOT / "earnsai/signals/schema.py").exists(),
        "risk_gate": (ROOT / "earnsai/risk/gate.py").exists(),
        "journal": (ROOT / "earnsai/journal/jsonl_store.py").exists(),
        "freqtrade_strategy": (ROOT / "freqtrade_user_data/strategies/EarnsAIJsonSignalStrategy.py").exists(),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("DOCTOR FAIL missing=" + ",".join(failed))
        raise SystemExit(1)
    print(f"DOCTOR PASS python={sys.version.split()[0]} root={ROOT}")

if __name__ == "__main__":
    main()
