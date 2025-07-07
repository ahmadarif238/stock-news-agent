import time
from config import BOT_TOKEN, CHAT_ID, RSS_FEEDS
from ticker_loader import load_tickers_from_file
from news_fetcher import fetch_news_from_rss
from relevance_evaluator import evaluate_news_with_llm
from telegram_bot import send_telegram_alert
from logger import log_alert

# Load the prompt template from file
with open("prompts/impact_prompt.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

seen_links = set()

# --- Helper to safely extract response components ---
def parse_llm_response(response):
    summary = ""
    impact = ""
    for line in response.splitlines():
        line = line.strip()
        if line.startswith("Summary:"):
            summary = line[len("Summary:"):].strip()
        elif line.startswith("Impact:"):
            impact = line[len("Impact:"):].strip()
    return summary, impact

# --- Main loop ---
def main():
    while True:
        tickers = load_tickers_from_file("tickers.txt")
        news_items = fetch_news_from_rss(tickers, RSS_FEEDS)

        for item in news_items:
            if item["link"] not in seen_links:
                result = evaluate_news_with_llm(item, prompt_template)

                # Debug print (optional)
                print("\n=== LLM Response ===")
                print(result)
                print("====================\n")

                summary, impact = parse_llm_response(result)

                if summary and impact:
                    send_telegram_alert(BOT_TOKEN, CHAT_ID, item["ticker"], summary, item["link"], impact)
                    log_alert(item["ticker"], summary, item["link"], impact)
                else:
                    print(f"⚠️ Skipping malformed response:\n{result}")

                seen_links.add(item["link"])

        time.sleep(600)  # check every 10 minutes

if __name__ == "__main__":
    main()
