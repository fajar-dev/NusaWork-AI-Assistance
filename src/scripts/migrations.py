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

    dsn = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
    )

    conn = None
    try:
        conn = await asyncpg.connect(dsn)

        async with conn.transaction():
            # Extensions
            print("Enabling extensions...")
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            await conn.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")  # gen_random_uuid()

            # Enum type for bot_type (idempotent)
            print("Ensuring bot_type enum exists...")
            await conn.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_type WHERE typname = 'bot_type_enum'
                ) THEN
                    CREATE TYPE bot_type_enum AS ENUM ('nusawork', 'nusaid');
                END IF;
            END$$;
            """)

            # Histories table (create if missing)
            print("Creating histories table...")
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS histories (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                similarity_score DOUBLE PRECISION DEFAULT NULL,
                similarity_results JSONB NULL,
                users JSON NOT NULL,
                space JSON NULL,
                bot_type bot_type_enum NOT NULL DEFAULT 'nusawork',
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            """)

            # Embeddings tables
            print("Creating nusawork embeddings table...")
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS nusawork_embeddings (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                content TEXT NOT NULL,
                vector vector(768) NOT NULL,
                metadata JSONB NULL
            );
            """)

            print("Creating nusaid embeddings table...")
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS nusaid_embeddings (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                content TEXT NOT NULL,
                vector vector(768) NOT NULL,
                metadata JSONB NULL
            );
            """)

        print("Migrations applied successfully.")

    except Exception as e:
        print(f"Error executing migrations: {e}")
        raise
    finally:
        if conn:
            await conn.close()
            
if __name__ == "__main__":
    asyncio.run(run_migrations())
