"""
Database configuration and session management.

Provides SQLAlchemy engine, session factory, declarative base,
and a FastAPI dependency for database sessions.

Caller must ensure all model modules are imported before calling
init_db(), so that Base.metadata is fully populated when
create_all() executes.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env from repository root
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Add DATABASE_URL=your_connection_string to the .env file "
        "in the repository root."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables registered on Base.metadata.

    Models must be imported by the caller before invoking this function
    so that their table definitions are present in Base.metadata.
    """
    Base.metadata.create_all(bind=engine)
