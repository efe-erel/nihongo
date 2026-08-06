
from fastapi import APIRouter
from app.schemas.furigana import FuriganaResponse, FuriganaRequest
from app.services.furigana import analyze_text


router = APIRouter()

@router.post("/furigana", response_model=FuriganaResponse)
def get_furigana(request: FuriganaRequest):
    tokens = analyze_text(request.text)
    return FuriganaResponse(tokens=tokens)