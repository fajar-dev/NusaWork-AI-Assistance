from sqlalchemy import Column, Integer, Text, Float, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import JSONB
from src.core.database import Base

class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    similarity_score = Column(Float, nullable=True)

    similarity_results = Column(JSONB, nullable=True)
    users = Column(JSONB, nullable=False)
    space = Column(JSONB, nullable=True)
    space = Column(JSONB, nullable=True)
    
    bot_type = Column(Enum("nusawork", "nusaid", name="bot_type_enum"), nullable=False, server_default="nusawork")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
