import requests
import html

def send_telegram_alert(bot_token, chat_id, ticker, summary, link, impact):
    # Escape HTML-sensitive characters and emojis
    safe_summary = html.escape(summary)
    safe_impact = ''.join(c for c in impact if ord(c) < 10000)

    message = f"""
<b>{ticker}</b>

<b>Summary:</b> {safe_summary}

🔗 <a href="{link}">Read more</a>

<b>Impact:</b> {safe_impact}
""".strip()

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage", 
        data=payload
    )

    if not response.ok:
        print("Telegram error:", response.text)
