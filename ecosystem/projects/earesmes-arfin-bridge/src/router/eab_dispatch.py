
from eab_manual_intake import EABManualIntakeHandler

manual_handler = EABManualIntakeHandler()

def dispatch_earesmes_turn(chat_id: str, text: str, fake_now_sec=None):
    res = manual_handler.handle_turn(chat_id, text, fake_now_sec=fake_now_sec)
    if res.get("handled"):
        return res
    return {
        "handled": False,
        "route": "EXACT_LKG_FALLTHROUGH"
    }
