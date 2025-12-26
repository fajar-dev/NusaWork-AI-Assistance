from __future__ import annotations

from langchain_postgres import PGEngine, PGVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from src.core.config import settings

TABLE_NAME = "embeddings"
ID_COLUMN = "id"
CONTENT_COLUMN = "content"
VECTOR_COLUMN = "vector"
METADATA_JSON_COLUMN = "metadata"


class VectorService:
    def __init__(self) -> None:
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.GOOGLE_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )
        self.engine = PGEngine.from_connection_string(settings.PSYCOPG_DATABASE_URL)

        vector_size = self._detect_vector_size(default_size=768)
        self._init_table(vector_size)

    def _detect_vector_size(self, default_size: int = 768) -> int:
        try:
            dim = len(self.embeddings.embed_query("dimension_check"))
            print(f"[VectorService] embedding dimension = {dim}")
            return dim
        except Exception:
            return default_size

    def _store_kwargs(self) -> dict:
        return {
            "table_name": TABLE_NAME,
            "id_column": ID_COLUMN,
            "content_column": CONTENT_COLUMN,
            "embedding_column": VECTOR_COLUMN,
            "metadata_json_column": METADATA_JSON_COLUMN,
        }

    def _init_table(self, vector_size: int) -> None:
        try:
            self.engine.init_vectorstore_table(
                vector_size=vector_size,
                **self._store_kwargs(),
            )
        except Exception as e:
            print(f"[VectorService] Table init skipped (likely exists): {e}")

    def get_vector_store(self) -> PGVectorStore:
        return PGVectorStore.create_sync(
            engine=self.engine,
            embedding_service=self.embeddings,
            **self._store_kwargs(),
        )

    def seed_data(self) -> None:
        print("[VectorService] Seeding data...")
        vector_store = self.get_vector_store()

        docs = [
            Document(
                page_content="NusaWork is a comprehensive HR management platform designed to streamline human resource processes.",
                metadata={"source": "overview"},
            ),
            Document(
                page_content="Features of NusaWork include attendance tracking, payroll management, and performance reviews.",
                metadata={"source": "features"},
            ),
            Document(
                page_content="NusaWork offers a mobile app for employees to check in/out and view their payslips.",
                metadata={"source": "mobile"},
            ),
            Document(
                page_content="The pricing for NusaWork starts at $10 per user per month for the basic plan.",
                metadata={"source": "pricing"},
            ),
            Document(
                page_content="You can contact NusaWork support via email at support@nusawork.com.",
                metadata={"source": "contact"},
            ),
        ]

        vector_store.add_documents(docs)
        print(f"[VectorService] Data seeded successfully! inserted={len(docs)}")


vector_service = VectorService()
