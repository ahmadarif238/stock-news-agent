import os
from datetime import datetime

def log_alert(ticker, summary, link, impact, log_path="logs/alerts.txt"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        f.write(f"Ticker: {ticker}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Impact: {impact}\n")
        f.write(f"Link: {link}\n")
        f.write("-" * 50 + "\n")
