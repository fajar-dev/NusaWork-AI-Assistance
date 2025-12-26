from pydantic import BaseModel
from typing import List, Optional, Any

class Source(BaseModel):
    content: str
    metadata: dict
    score: float

class AskRequest(BaseModel):
    users: object
    space: Optional[object] = None
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
