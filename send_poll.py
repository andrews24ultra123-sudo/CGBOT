import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# HARD-CODED TOKEN & CHAT ID
TOKEN = "8241808848:AAH_Qw-53tbVqT-er8lU-beUI2U2cuUsncE"   # your token
CHAT_ID = "54380770"  # your chat id (string, works fine)

SGT = ZoneInfo("Asia/Singapore")
now_sgt = datetime.now(SGT)
weekday = now_sgt.weekday()  # Monday=0 ... Sunday=6

if weekday == 5:  # Saturday
    target_date = (now_sgt + timedelta(days=1)).date()  # Sunday
    question = f"Sunday Service – {target_date:%Y-%m-%d (%a)}"
    options = ["9am", "11.15am", "Serving", "Lunch", "Invited a friend"]
    allows_multiple_answers = True
elif weekday == 2:  # Wednesday
    target_date = (now_sgt + timedelta(days=2)).date()  # Friday
    question = f"Cell Group – {target_date:%Y-%m-%d (%a)}"
    options = ["Dinner 7.15pm", "CG 8.15pm", "Cannot make it"]
    allows_multiple_answers = False
else:
    print("Not Wednesday or Saturday, exiting.")
    exit(0)

url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
payload = {
    "chat_id": CHAT_ID,
    "question": question,
    "options": json.dumps(options),
    "is_anonymous": False,
    "allows_multiple_answers": allows_multiple_answers,
}

resp = requests.post(url, data=payload, timeout=30)
if resp.ok:
    print("Poll sent successfully:", question)
else:
    print("Poll failed:", resp.status_code, resp.text)
