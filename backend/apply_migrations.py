import os
import glob
from dotenv import load_dotenv
from sqlalchemy import text
from app.core.database import engine

load_dotenv()

def apply_migrations():
    migration_files = sorted(glob.glob("migrations/*.sql"))
    if not migration_files:
        print("No migration files found.")
        return

    with engine.connect() as conn:
        for filepath in migration_files:
            if "._" in filepath: continue # skip macos hidden files
            print(f"Applying {filepath}...")
            with open(filepath, "r") as f:
                sql = f.read()
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"  Success: {filepath}")
                except Exception as e:
                    print(f"  Error in {filepath}: {e}")
                    conn.rollback()

if __name__ == "__main__":
    apply_migrations()
