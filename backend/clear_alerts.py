from sqlmodel import Session, select
from app.database import engine
from app.models import NewsAlert

def clear_alerts():
    with Session(engine) as session:
        alerts = session.exec(select(NewsAlert)).all()
        for alert in alerts:
            session.delete(alert)
        session.commit()
    print("Database alerts cleared.")

if __name__ == "__main__":
    clear_alerts()
