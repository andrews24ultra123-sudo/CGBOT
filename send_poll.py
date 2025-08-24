import os
import json
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ========= HARD-CODED CREDENTIALS (as requested) =========
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"  # keep as string; Telegram accepts it

# ========= OPTIONAL OVERRIDES FROM WORKFLOW INPUTS =========
# These are only used in TEST mode (so you can click "Run workflow" and customize)
MODE = os.environ.get("MODE", "").upper()           # TEST | SAT | WED (only set when manual run)
CHAT_ID_OVERRIDE = os.environ.get("CHAT_ID_OVERRIDE", "").strip()
CUSTOM_QUESTION = os.environ.get("CUSTOM_QUESTION", "Test Poll – does this work?")
CUSTOM_OPTIONS = os.environ.get("CUSTOM_OPTIONS", "Yes,No")
ALLOW_MULTI = os.environ.get("ALLOW_MULTI", "false").lower() == "true"

# ========= TIMEZONE =========
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
    resp = requests.post(url, data=payload, timeout=30)
    if not resp.ok:
        raise SystemExit(f"sendPoll failed: {resp.status_code} {resp.text}")
    print("Poll sent:", question)

def run_sat():
    # Saturday 6pm SGT -> poll for Sunday (T+1)
    target_date = (now_sgt + timedelta(days=1)).date()
    q = f"Sunday Service – {target_date:%Y-%m-%d (%a)}"
    opts = ["9am", "11.15am", "Serving", "Lunch", "Invited a friend"]
    send_poll(q, opts, allows_multi=True, chat_id=CHAT_ID)

def run_wed():
    # Wednesday 6pm SGT -> poll for Friday (T+2)
    target_date = (now_sgt + timedelta(days=2)).date()
    q = f"Cell Group – {target_date:%Y-%m-%d (%a)}"
    opts = ["Dinner 7.15pm", "CG 8.15pm", "Cannot make it"]
    send_poll(q, opts, allows_multi=False, chat_id=CHAT_ID)

def run_test():
    # TEST mode lets you choose question/options from the workflow UI
    chat_id = CHAT_ID_OVERRIDE if CHAT_ID_OVERRIDE else CHAT_ID
    opts = [s.strip() for s in CUSTOM_OPTIONS.split(",") if s._]()
