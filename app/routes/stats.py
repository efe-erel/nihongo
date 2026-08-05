
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.word import Word
from app.models.review_log import ReviewLog
from app.schemas.stats import StatsResponse

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_words = db.query(Word).count()
    total_reviews = db.query(ReviewLog).count()
    correct_reviews = db.query(ReviewLog).filter(ReviewLog.quality >= 3).count()

    accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0.0

    return StatsResponse(
        total_words=total_words,
        total_reviews=total_reviews,
        accuracy=round(accuracy, 1)
    )