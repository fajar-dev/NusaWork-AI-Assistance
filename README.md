# NusaAI RAG System

A Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, Google Gemini, and PostgreSQL (pgvector).

## Features

- **RAG Architecture**: Retrieves relevant context from vector storage to answer user questions.
- **Google Gemini**: for generation and vector embeddings.
- **PostgreSQL**: Robust database with `pgvector` extension for similarity search.
- **Conversation History**: Logs all questions, answers, and retrieved context.

## Project Structure

```
├── main.py                # Application entry point
├── requirements.txt       # Dependencies
├── .env                   # Configuration
└── src/
    ├── core/              # Config & Database
    ├── models/            # SQLAlchemy Models
    ├── schemas/           # Pydantic Schemas
    ├── services/          # Business Logic (RAG, Vector)
    ├── api/               # API Routes
    └── scripts/           # Migrations & Seeding
```

## Prerequisites

- **Python 3.11** (Required due to compatibility issues with newer versions)
- PostgreSQL with `pgvector` extension

## Setup & Installation

1.  **Clone the repository** (if applicable).
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    Create a `.env` file in the root directory:

    ```env
    PORT=8000
    HOST=0.0.0.0

    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=password
    DB_DATABASE=vectordb

    GOOGLE_API_KEY=your_google_api_key
    GOOGLE_EMBEDDING_MODEL=embedding-001
    GOOGLE_LLM_MODEL=gemini-pro
    KWARGS=3
    ```

## Running with Docker

1.  **Build and Start**:
    ```bash
    docker-compose up --build
    ```
2.  **Run Migrations**:
    ```bash
    docker-compose exec app python -m src.scripts.migrations
    ```
3.  **Seed Data**:
    ```bash
    docker-compose exec app python -m src.scripts.seed
    ```
4.  **Access**:
    The API will be available at `http://localhost:8000`.

## Usage

### 1. Database Setup

Initialize the database and table:

```bash
python -m src.scripts.migrations
```

### 2. Seed Data

Populate the vector store with example content:

```bash
python -m src.scripts.nusawork_seed
python -m src.scripts.nusaid_seed
```

### 3. Run the Server

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 4. API Endpoints

**POST** `/ask-nusawork`

```json
{
  "question": "Cara ekspor data tren kehadiran?"
}
```

Response:

```json
{
  "question": "What allows employees to check in?",
  "answer": "NusaWork offers a mobile app...",
  "sources": [
    {
      "content": "NusaWork is a comprehensive HR management platform designed to streamline human resource processes.",
      "metadata": {
        "source": "overview"
      },
      "score": 0.4572025734098184
    }
  ]
}
```

**POST** `/ask-nusaid`

```json
{
  "question": "Apa itu NusaID?"
}
```

Response:

```json
{
  "question": "Apa itu NusaID?",
  "answer": "NusaID is... ",
  "sources": [
    {
      "content": "NusaWork is a comprehensive HR management platform designed to streamline human resource processes.",
      "metadata": {
        "source": "overview"
      },
      "score": 0.4572025734098184
    }
  ]
}
```
