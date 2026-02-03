from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Ticker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NewsAlert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True)
    title: str
    summary: str
    link: str = Field(unique=True)  # Prevent duplicate alerts
    impact: str  # e.g., "High", "Medium", "Bs"
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
