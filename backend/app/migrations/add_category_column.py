from app.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    print("Adding 'category' column to 'screenshots' table...")
    conn.execute(text(
        """
        ALTER TABLE screenshots ADD COLUMN IF NOT EXISTS category VARCHAR;
        """
    ))
    print("Done.") 