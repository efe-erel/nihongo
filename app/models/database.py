"""Database connection helpers."""

from pathlib import Path

from app.config import DATABASE_PATH


def get_database_path() -> Path:
    """Return the configured SQLite database path."""

    return DATABASE_PATH
