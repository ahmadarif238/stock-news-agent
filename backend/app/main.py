from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List

from app.database import create_db_and_tables, get_session
from app.models import Ticker, NewsAlert
from app.services.agent import run_agent_cycle
from fastapi.middleware.cors import CORSMiddleware

# --- Seeding ---
DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOGL", "NVDA", "AMZN", "MSFT", "NFLX", "META"]


def _seed_default_tickers():
    """Populate a watchlist on first boot.

    Without this an empty (or freshly fallen-back) database renders a blank
    dashboard, which reads as "broken" to anyone visiting the deployed demo.
    """
    from app.database import engine
    try:
        with Session(engine) as session:
            if session.exec(select(Ticker)).first():
                return  # already has data - leave the user's watchlist alone
            for symbol in DEFAULT_TICKERS:
                session.add(Ticker(symbol=symbol))
            session.commit()
            print(f"Seeded {len(DEFAULT_TICKERS)} default tickers.")
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: could not seed tickers: {exc}")


# --- Background Task Setup ---
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup. Every step is guarded: a portfolio deployment must come up even
    # if the database or an upstream news/LLM API is having a bad day.
    try:
        create_db_and_tables()
        _seed_default_tickers()
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: DB init failed at startup: {exc}")

    try:
        scheduler.add_job(run_agent_cycle, 'interval', minutes=10) # Run every 10 mins
        scheduler.start()
        run_agent_cycle() # Run once immediately on startup
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: agent cycle could not start: {exc}")

    yield

    # Shutdown
    try:
        scheduler.shutdown()
    except Exception:  # noqa: BLE001
        pass

app = FastAPI(lifespan=lifespan)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for now (dev), restrict for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/tickers", response_model=List[Ticker])
def get_tickers(session: Session = Depends(get_session)):
    return session.exec(select(Ticker)).all()

@app.post("/tickers", response_model=Ticker)
def add_ticker(ticker: Ticker, session: Session = Depends(get_session)):
    existing = session.exec(select(Ticker).where(Ticker.symbol == ticker.symbol)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ticker already exists")
    session.add(ticker)
    session.commit()
    session.refresh(ticker)
    # Trigger a cycle? maybe async
    return ticker

@app.delete("/tickers/{ticker_id}")
def delete_ticker(ticker_id: int, session: Session = Depends(get_session)):
    ticker = session.get(Ticker, ticker_id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    session.delete(ticker)
    session.commit()
    return {"ok": True}

@app.get("/alerts", response_model=List[NewsAlert])
def get_alerts(session: Session = Depends(get_session)):
    # Return latest 50 alerts
    return session.exec(select(NewsAlert).order_by(NewsAlert.created_at.desc()).limit(50)).all()
