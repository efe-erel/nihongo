from fastapi import FastAPI
from app.models.database import Base, engine
from app.models import word, review_log

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"test"}