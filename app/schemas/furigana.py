
from pydantic import BaseModel

class FuriganaRequest(BaseModel):
    text: str


class FuriganaToken(BaseModel):
    surface: str
    reading: str
    has_kanji: bool


class FuriganaResponse(BaseModel):
    tokens: list[FuriganaToken]