"""
Shared pytest fixtures.

Uses an in-memory SQLite database so tests run without a live PostgreSQL instance.

Strategy:
  - Patch app.core.database.engine and SessionLocal to SQLite equivalents
    BEFORE the FastAPI TestClient triggers the lifespan (which calls
    Base.metadata.create_all via _db_module.engine).
  - The patch_engine fixture is session-scoped and auto-used, so it runs
    before the first client fixture is created.
"""
import os
os.environ.setdefault("DATABASE_URL", "sqlite://")   # prevent real DB connection at import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.core.database as db_module
from app.core.database import Base, get_db
from app.main import app

SQLITE_URL = "sqlite://"   # pure in-memory

_engine_test = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=_engine_test)


@pytest.fixture(scope="session", autouse=True)
def patch_engine():
    """
    Replace the module-level engine and SessionLocal with SQLite equivalents
    for the entire test session.  This ensures:
      - main.py lifespan create_all uses SQLite
      - health router's SessionLocal() uses SQLite
      - all get_db dependency calls use SQLite
    """
    original_engine = db_module.engine
    original_session_local = db_module.SessionLocal

    db_module.engine = _engine_test
    db_module.SessionLocal = _TestingSession

    Base.metadata.create_all(bind=_engine_test)
    yield
    Base.metadata.drop_all(bind=_engine_test)

    db_module.engine = original_engine
    db_module.SessionLocal = original_session_local


@pytest.fixture()
def db(patch_engine):
    session = _TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
