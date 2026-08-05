
from pydantic import BaseModel
from datetime import date, datetime


class WordCreate(BaseModel):
    kanji: str
    reading: str
    meaning: str


class WordResponse(BaseModel):
    id: int
    kanji: str
    reading: str
    meaning: str
    repetitions: int
    interval: int
    ease_factor: float
    next_review_date: date
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewAnswer(BaseModel):
    quality: int