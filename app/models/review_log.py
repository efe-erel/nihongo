"""Review history model definition."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewLog:
    id: int | None = None
    word_id: int | None = None
    user_id: int | None = None
    reviewed_at: datetime | None = None
    quality: int | None = None
