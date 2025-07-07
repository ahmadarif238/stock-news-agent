📈 Real-Time Stock News Alert AI Agent
A fully modular AI-powered agent that tracks real-time stock news, evaluates impact using a language model (Groq + LLaMA3), and sends alerts via Telegram.


## 🚀 Features

- ✅ Tracks important stock-related news via RSS
- ✅ Evaluates market impact (1–5 sirens) using LLM
- ✅ Sends alerts with ticker, summary, impact, and article link
- ✅ Uses `tickers.txt` to define watchlist
- ✅ Modular and upgradable

## 🧠 How It Works

1. Pulls latest news from finance RSS feeds
2. Filters news mentioning tickers from `tickers.txt`
3. Sends summary + title to LLM with an analysis prompt
4. Parses LLM output → sends formatted alert to Telegram
5. Logs everything in `logs/alerts.txt`

## 📦 Folder Structure

```bash
project/
├── main.py                # Main execution loop
├── config.py              # Configs, tokens, RSS feeds
├── ticker_loader.py       # Loads tickers from file
├── news_fetcher.py        # RSS news fetch logic
├── relevance_evaluator.py # LLM evaluation via Groq
├── telegram_bot.py        # Alert messaging to Telegram
├── logger.py              # Logs alerts to file
├── prompts/impact_prompt.txt
├── logs/alerts.txt
├── tickers.txt            # List of stock tickers to track
├── requirements.txt
├── .env                   # API keys
```

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/stock-news-agent.git
cd stock-news-agent
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your `.env`
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### 5. Add Tickers
Edit the `tickers.txt` file with 1 ticker per line (e.g., AAPL, TSLA, GOOGL)

### 6. Run the Agent
```bash
python main.py
```

## 📬 Telegram Output Format
```
📈 Ticker: TSLA
📄 Summary: Tesla’s stock jumped after a record delivery report.
🚨 Impact: 🚨🚨🚨🚨
🔗 Link: https://finance.yahoo.com/news/tesla...
```

## 🧠 Powered By
- Groq API (LLaMA3 8B)
- Telegram Bot API
- Python + RSS parsing

## 🔄 Upgrade Ideas
- Add Google Sheets integration for tickers
- Export data to CSV/DB
- Build a web dashboard with Flask + React
