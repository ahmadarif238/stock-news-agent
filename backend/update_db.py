from sqlalchemy import text
from app.database import engine

def update_schema():
    with engine.connect() as conn:
        print("Checking for image_url column...")
        try:
            conn.execute(text("ALTER TABLE newsalert ADD COLUMN image_url VARCHAR;"))
            conn.commit()
            print("Successfully added image_url column.")
        except Exception as e:
            if "already exists" in str(e):
                print("Column image_url already exists.")
            else:
                print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_schema()
