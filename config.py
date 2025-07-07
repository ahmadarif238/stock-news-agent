import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RSS_FEEDS = [
    "https://finance.yahoo.com/rss/topstories",
    "https://www.marketwatch.com/rss/topstories"
]