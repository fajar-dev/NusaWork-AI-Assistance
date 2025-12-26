import asyncio
import asyncpg
from src.core.config import settings

async def create_database_if_not_exists():
    sys_dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    try:
        conn = await asyncpg.connect(sys_dsn)
        exists = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_DATABASE}'")
        if not exists:
            print(f"Database '{settings.DB_DATABASE}' does not exist. Creating...")
            await conn.execute(f'CREATE DATABASE "{settings.DB_DATABASE}"')
            print(f"Database '{settings.DB_DATABASE}' created.")
        else:
            print(f"Database '{settings.DB_DATABASE}' already exists.")
        await conn.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

async def run_migrations():
    await create_database_if_not_exists()

    print("Running migrations...")
    
    dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
    
    try:
        conn = await asyncpg.connect(dsn)
        
        print("Enabling vector extension...")
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        print("Creating history table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS histories (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            similarity_score FLOAT DEFAULT NULL,
            similarity_results JSONB NULL,
            users JSON NOT NULL,
            space JSON NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        await conn.execute(create_table_query)
        
        print("Migrations applied successfully.")
        
    except Exception as e:
        print(f"Error executing migrations: {e}")
    finally:
        if 'conn' in locals() and conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(run_migrations())
