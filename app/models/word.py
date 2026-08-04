"""Word model definition."""

from dataclasses import dataclass


@dataclass
class Word:
    id: int | None = None
    japanese: str = ""
    english: str = ""
    notes: str = ""
