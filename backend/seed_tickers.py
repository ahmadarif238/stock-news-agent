from sqlmodel import Session, select
from app.database import engine
from app.models import Ticker

DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOGL", "NVDA", "AMZN", "MSFT", "NFLX", "META", "BABA", "T"]

def seed_tickers():
    with Session(engine) as session:
        for symbol in DEFAULT_TICKERS:
            existing = session.exec(select(Ticker).where(Ticker.symbol == symbol)).first()
            if not existing:
                print(f"Adding {symbol}...")
                session.add(Ticker(symbol=symbol))
        session.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_tickers()
