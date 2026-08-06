from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.word import Word
from app.models.review_log import ReviewLog
from app.schemas.stats import StatsResponse
from app.services.stats import calculate_streak

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_words = db.query(Word).count()
    total_reviews = db.query(ReviewLog).count()
    correct_reviews = db.query(ReviewLog).filter(ReviewLog.quality >= 3).count()

    accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0.0

    raw_dates = db.query(func.date(ReviewLog.review_date)).distinct().all()
    review_dates = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in raw_dates]
    current_streak = calculate_streak(review_dates)

    return StatsResponse(
        total_words=total_words,
        total_reviews=total_reviews,
        accuracy=round(accuracy, 1),
        current_streak=current_streak
    )