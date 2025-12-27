from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings

from src.models.history import History
from fastapi import Depends
from src.services.vector_service import VectorService, get_vector_service

class RAGService:
    def __init__(self, vector_service):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GOOGLE_LLM_MODEL, 
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.vector_store = vector_service.get_vector_store()
        
        self.template = """Answer the question based only on the following context.

        Context:
        {context}

        Question:
        {question}

        Instruction:
        - Answer briefly, clearly, and directly with Indonesian language.
        - Use only information from the context.
        """

        self.prompt = ChatPromptTemplate.from_template(self.template)

    def _format_docs(self, docs):
        return "\n\n".join([d.page_content for d in docs])

    async def ask_question(self, question: str, users: object, space: object, db: AsyncSession) -> dict:
        # 1. Retrieve with scores
        docs_and_scores = self.vector_store.similarity_search_with_score(question, k=settings.KWARGS)
        
        docs = [doc for doc, _ in docs_and_scores]
        context_text = self._format_docs(docs)
        
        # Prepare sources for response and history
        sources_data = []
        for doc, score in docs_and_scores:
            sources_data.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        

        # 2. Generate
        chain = (
            RunnablePassthrough() 
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )
        answer = await chain.ainvoke({"context": context_text, "question": question})

        # 3. Save History
        new_history = History(
            question=question,
            answer=answer,
            users=users,
            space=space,
            similarity_score=sources_data[0]["score"] if sources_data else 0.0,
            similarity_results=sources_data
        )
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources_data
        }

def get_rag_service(vector_service: VectorService = Depends(get_vector_service)):
    return RAGService(vector_service)

