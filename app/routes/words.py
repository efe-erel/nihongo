"""Word CRUD routes."""

from fastapi import APIRouter


router = APIRouter(prefix="/words", tags=["words"])


@router.get("")
def list_words() -> list[dict[str, str]]:
    return []
