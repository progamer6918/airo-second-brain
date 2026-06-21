import argparse
import json

from airo_personal_workflow.telegram.local_handler import handle_telegram_text


def handle_text(text: str) -> dict:
    return handle_telegram_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Airo Personal Workflow Gateway")
    parser.add_argument("text", nargs="+", help="User message text")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON")
    args = parser.parse_args()

    text = " ".join(args.text)
    result = handle_text(text)

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
