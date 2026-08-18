"""Application settings, loaded from environment variables / the .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root (the directory containing app/, frontend/, data/, .env).
BASE_DIR = Path(__file__).resolve().parents[1]

SQLITE_PREFIX = "sqlite:///"


class Settings(BaseSettings):
    """Runtime configuration.

    Every field falls back to a local-development default, so the app still
    runs correctly when no .env file is present.
    """

    # SQLite file inside data/ by default. Override in .env to point at another
    # database (e.g. postgresql+psycopg://... in production).
    database_url: str = f"{SQLITE_PREFIX}{(BASE_DIR / 'data' / 'app.db').as_posix()}"

    model_config = SettingsConfigDict(
        # Absolute path, so the .env file is found no matter which directory
        # uvicorn is started from.
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        # .env also holds frontend-only keys (API_URL); ignore anything that is
        # not a field on this class instead of raising a validation error.
        extra="ignore",
    )

    @property
    def resolved_database_url(self) -> str:
        """The database URL with relative SQLite paths anchored to the project root.

        Without this, ``sqlite:///data/app.db`` would resolve against the current
        working directory, and starting the server from another folder would
        silently create a second, empty database.
        """
        if not self.database_url.startswith(SQLITE_PREFIX):
            return self.database_url

        path_part = self.database_url[len(SQLITE_PREFIX):]

        # Absolute path (sqlite:////abs/path) or in-memory database: use as-is.
        if not path_part or path_part.startswith("/") or ":memory:" in path_part:
            return self.database_url

        return f"{SQLITE_PREFIX}{(BASE_DIR / path_part).resolve().as_posix()}"


settings = Settings()
