import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {url}")

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Success:", result.fetchone())
except Exception as e:
    with open("error.log", "w") as f:
        f.write(str(e))
    print("Error logged to error.log")
