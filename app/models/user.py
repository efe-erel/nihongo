"""User model definition."""

from dataclasses import dataclass


@dataclass
class User:
    id: int | None = None
    name: str = "default"
