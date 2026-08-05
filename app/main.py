from fastapi import FastAPI
from app.models.database import Base, engine
from app.models import word, review_log
from app.routes import words, review, stats

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(words.router)
app.include_router(stats.router)
app.include_router(review.router)

@app.get("/")
def read_root():
    return {"test"}