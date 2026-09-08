"""
01_create_schema.py
-------------------
Creates all database tables from the SQLAlchemy ORM models.
Run once before seeding.

Usage:
    python scripts/01_create_schema.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import Base, engine
import app.models  # noqa: F401 — registers all models with Base

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print(f"Done — {len(Base.metadata.tables)} tables created/verified.")
    for t in sorted(Base.metadata.tables):
        print(f"  ✓ {t}")

if __name__ == "__main__":
    main()
