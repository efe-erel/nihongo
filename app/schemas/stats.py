from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_words: int
    total_reviews: int
    accuracy: int