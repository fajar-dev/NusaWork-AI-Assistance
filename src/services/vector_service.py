from __future__ import annotations

from langchain_postgres import PGEngine, PGVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.core.config import settings

ID_COLUMN = "id"
CONTENT_COLUMN = "content"
VECTOR_COLUMN = "vector"
METADATA_JSON_COLUMN = "metadata"


class VectorService:
    def __init__(self) -> None:
        self.engine = PGEngine.from_connection_string(settings.PSYCOPG_DATABASE_URL)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.GOOGLE_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )

        # vector_size = self._detect_vector_size(default_size=768)
        # self._init_table(vector_size)


    def _store_kwargs(self, table_name: str) -> dict:
        return {
            "table_name": table_name,
            "id_column": ID_COLUMN,
            "content_column": CONTENT_COLUMN,
            "embedding_column": VECTOR_COLUMN,
            "metadata_json_column": METADATA_JSON_COLUMN,
        }

    def get_vector_store(self, table_name: str) -> PGVectorStore:
        return PGVectorStore.create_sync(
            engine=self.engine,
            embedding_service=self.embeddings,
            **self._store_kwargs(table_name),
        )

    def get_nusawork_store(self) -> PGVectorStore:
        return self.get_vector_store("nusawork_embeddings")
    
    def get_nusaid_store(self) -> PGVectorStore:
        return self.get_vector_store("nusaid_embeddings")


def get_vector_service():
    return VectorService()

