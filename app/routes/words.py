
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.word import Word
from app.schemas.word import WordCreate, WordResponse
from app.models.review_log import ReviewLog

router = APIRouter()


@router.post("/words", response_model=WordResponse)
def create_word(word: WordCreate, db: Session = Depends(get_db)):
    new_word = Word(
        kanji=word.kanji,
        reading=word.reading,
        meaning=word.meaning
    )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word


@router.get("/words", response_model=list[WordResponse])
def get_words(db: Session = Depends(get_db)):
    return db.query(Word).all()


from app.models.review_log import ReviewLog

@router.delete("/words/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    db.query(ReviewLog).filter(ReviewLog.word_id == word_id).delete()
    db.delete(word)
    db.commit()
    return {"detail": "Word deleted"}