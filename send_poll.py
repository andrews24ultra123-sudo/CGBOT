import os
import json
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ========= HARD-CODED CREDENTIALS =========
TOKEN = "8241808848:AAH_Qw-53tbVqT-er8lU-beUI2U2cuUsncE"
CHAT_ID = "54380770"  # your group id

# ========= OPTIONAL OVERRIDES FROM WORKFLOW INPUTS =========
MODE = os.environ.get("MODE", "").upper()           # TEST | SAT | WED
CHAT_ID_OVERRIDE = os.environ.get("CHAT_ID_OVERRIDE", "").strip()
CUSTOM_QUESTION = os.environ.get("CUSTOM_QUESTION", "Test Poll – does this work?")
CUSTOM_OPTIONS = os.environ.get("CUSTOM_OPTIONS", "Yes,No")
ALLOW_MULTI = os.environ.get("ALLOW_MULTI", "false").lower() == "true"

SGT = ZoneInfo("Asia/Singapore")
now_sgt = datetime.now(SGT)
weekday = now_sgt.weekday()  # Monday=0 ... Sunday=6

def send_poll(question: str, options_list, allows_multi: bool, chat_id: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
    payload = {
        "chat_id": chat_id,
        "question": question,
        "options": json.dumps(options_list),
        "is_anonymous": False,
        "allows_multiple_answers": allows_multi,
    }
    re
