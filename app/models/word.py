
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime, date
from app.models.database import Base
from sqlalchemy.orm import relationship

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(String, nullable=False)
    reading = Column(String, nullable=False)
    meaning = Column(String, nullable=False)

    ease_factor = Column(Float, default=2.5)
    repetitions = Column(Integer, default=0)
    interval = Column(Integer, default=0)
    next_review_date = Column(Date, default=date.today)

    created_at = Column(DateTime, default=datetime.utcnow)

    review_logs = relationship("ReviewLog", back_populates="word")
