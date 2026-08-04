"""Review routes."""

from fastapi import APIRouter


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/today")
def get_today_reviews() -> list[dict[str, str]]:
    return []
