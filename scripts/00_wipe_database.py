"""
00_wipe_database.py
-------------------
Drops and recreates all tables — complete data wipe.
Run this ONCE before reseeding with exact target numbers.

Usage:
    python scripts/00_wipe_database.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import Base, engine
import app.models  # noqa: F401 — registers all models

def main():
    confirm = input(
        "\n⚠️  This will DELETE ALL DATA in the database.\n"
        "Type YES to confirm: "
    ).strip()
    if confirm != "YES":
        print("Aborted.")
        return

    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done — database is clean and ready for seeding.")

if __name__ == "__main__":
    main()
