import logging
from sqlmodel import Session, select
from app.database import engine
from app.models import Ticker, NewsAlert
from app.services.news_service import fetch_news_from_rss
from app.services.llm_service import evaluate_news

logger = logging.getLogger(__name__)

def run_agent_cycle():
    """
    1. Load tickers from DB.
    2. Fetch news.
    3. Filter checked links (optimization: check DB).
    4. Evaluate with LLM.
    5. Save alerts to DB.
    """
    print("Running Agent Cycle...")
    with Session(engine) as session:
        # 1. Get tickers
        tickers = session.exec(select(Ticker)).all()
        ticker_list = [t.symbol for t in tickers]
        
        if not ticker_list:
            print("No tickers to track.")
            return

        # 2. Fetch News
        news_items = fetch_news_from_rss(ticker_list)
        
        for item in news_items:
            # 3. Check duplicate links
            # Optimization: We could cache this or do a bulk check
            existing = session.exec(select(NewsAlert).where(NewsAlert.link == item["link"])).first()
            if existing:
                continue
            
            # 4. Evaluate
            print(f"Evaluating news for {item['ticker']}...")
            evaluation = evaluate_news(item["ticker"], item["title"], item["summary"])
            
            # 5. Save
            alert = NewsAlert(
                ticker=item["ticker"],
                title=item["title"],
                summary=evaluation["summary"],
                link=item["link"],
                impact=evaluation["impact"],
                image_url=item["image_url"]
            )
            session.add(alert)
            session.commit()
            print(f"Saved alert for {item['ticker']}")
