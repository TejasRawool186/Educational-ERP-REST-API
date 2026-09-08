"""
00_wipe_database.py
-------------------
Wipes all data by dropping and recreating the public schema.
Uses raw SQL to bypass SQLAlchemy's circular FK dependency issue
between departments ↔ faculty.

Usage:
    python scripts/00_wipe_database.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from app.core.database import engine
import app.models  # noqa — registers all models with Base
from app.core.database import Base


def main():
    confirm = input(
        "\n⚠️  This will DELETE ALL DATA in the database.\n"
        "Type YES to confirm: "
    ).strip()
    if confirm != "YES":
        print("Aborted.")
        return

    with engine.begin() as conn:
        print("Dropping schema and all tables...")
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO PUBLIC"))
        print("Schema recreated cleanly.")

    print("Recreating tables from ORM models...")
    Base.metadata.create_all(bind=engine)
    print("Done — database is clean and ready for seeding.")


if __name__ == "__main__":
    main()
