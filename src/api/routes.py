from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.schemas.chat import AskRequest, AskResponse
from src.services.rag_service import RAGService, get_rag_service

router = APIRouter()

@router.post("/ask-nusawork", response_model=AskResponse)
async def ask_nusawork(
    request: AskRequest, 
    db: AsyncSession = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service)
):
    try:
        result = await rag_service.ask_question(request.question, request.users, request.space, 'nusawork', db)
        return AskResponse(**result)
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask-nusaid", response_model=AskResponse)
async def ask_nusaid(
    request: AskRequest, 
    db: AsyncSession = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service)
):
    try:
        result = await rag_service.ask_question(request.question, request.users, request.space, 'nusaid', db)
        return AskResponse(**result)
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

