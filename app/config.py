"""Application configuration helpers."""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = Path(os.getenv("APP_DATABASE_PATH", DATA_DIR / "app.db"))
