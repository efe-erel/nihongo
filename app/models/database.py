
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import SQLITE_PREFIX, settings


DATABASE_URL = settings.resolved_database_url

# check_same_thread is a SQLite-only argument; skip it for any other backend.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Make sure the directory holding the SQLite file exists (data/ is gitignored,
# so it is missing right after a fresh clone).
if DATABASE_URL.startswith(SQLITE_PREFIX) and ":memory:" not in DATABASE_URL:
    Path(DATABASE_URL[len(SQLITE_PREFIX):]).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()