# schemas.py
from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    success: bool
    message: str

class AskRequest(BaseModel):
    question: str
    top_k: int = 4

class AnswerResponse(BaseModel):
    answer: str
    citations: List[dict]  # [{'page': int, 'text': '...'}]
