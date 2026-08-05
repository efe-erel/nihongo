
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.word import Word
from app.models.review_log import ReviewLog
from app.schemas.word import WordResponse, ReviewAnswer
from app.services.srs import calculate_next_review
import random

router = APIRouter()


@router.get("/review/today", response_model=list[WordResponse])
def get_todays_reviews(db: Session = Depends(get_db)):
    today = date.today()
    words = db.query(Word).filter(Word.next_review_date <= today).all()
    random.shuffle(words)
    return words


@router.post("/review/{word_id}/answer", response_model=WordResponse)
def submit_answer(word_id: int, answer: ReviewAnswer, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    try:
        new_repetitions, new_interval, new_ease_factor = calculate_next_review(
            quality=answer.quality,
            repetitions=word.repetitions,
            interval=word.interval,
            ease_factor=word.ease_factor
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    word.repetitions = new_repetitions
    word.interval = new_interval
    word.ease_factor = new_ease_factor
    word.next_review_date = date.today() + timedelta(days=new_interval)

    log_entry = ReviewLog(word_id=word.id, quality=answer.quality)
    db.add(log_entry)

    db.commit()
    db.refresh(word)
    return word