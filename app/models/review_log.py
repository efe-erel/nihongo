
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship
from app.models.database import Base

class ReviewLog(Base):
    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    quality = Column(Integer, nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow)

    word = relationship("Word", back_populates="review_logs")