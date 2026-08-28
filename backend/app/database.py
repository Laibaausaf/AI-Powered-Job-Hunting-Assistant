"""
SQLite database setup. For a hackathon, SQLite is plenty: it's a single file
(`jobhunt.db`), needs no server, and status changes persist across restarts,
which satisfies Module D's "must survive refresh/re-login" requirement.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# check_same_thread=False is needed because FastAPI can use SQLite from
# different threads within one process - safe for our single-file dev setup.
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
