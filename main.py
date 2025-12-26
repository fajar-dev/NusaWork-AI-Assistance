from fastapi import FastAPI
from src.api.routes import router as chat_router
import uvicorn

app = FastAPI(title="NusaWork RAG API")

app.include_router(chat_router)

from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
