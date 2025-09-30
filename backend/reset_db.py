import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def reset_database():
    try:
        # Check if URL is Render (remote) or local
        if "render.com" in DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        else:
            conn = psycopg2.connect(DATABASE_URL)  # Local Postgres, no SSL

        conn.autocommit = True
        cur = conn.cursor()

        # Truncate example table (replace with your tables)
        cur.execute("TRUNCATE TABLE stocks RESTART IDENTITY CASCADE;")
        cur.execute("TRUNCATE TABLE ticker_progress RESTART IDENTITY CASCADE;")

        print("✅ Database reset: all data cleared.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error resetting database: {e}")

if __name__ == "__main__":
    reset_database()