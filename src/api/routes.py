from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.chat import AskRequest, AskResponse
from src.services.rag_service import rag_service

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await rag_service.ask_question(request.question, request.users, request.space, db)
        return AskResponse(**result)
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
