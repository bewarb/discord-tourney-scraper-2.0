import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables (from .env if present)
load_dotenv()


def _require_env(name: str) -> str:
    """
    Read an environment variable and fail fast with a helpful error if missing.
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Add it to your .env file (or export it in your shell)."
        )
    return value


def connect_db():
    """
    Establish a connection to the PostgreSQL database using required env vars.
    """
    return psycopg2.connect(
        host=_require_env("DB_HOST"),
        database=_require_env("DB_NAME"),
        user=_require_env("DB_USER"),
        password=_require_env("DB_PASS"),
    )


def initialize_database():
    """
    Create the tournaments table if it doesn't exist.
    """
    conn = connect_db()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS tournaments (
        id SERIAL PRIMARY KEY,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        link TEXT NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        level TEXT,
        cost TEXT,
        max_teams INTEGER,
        confirmed INTEGER,
        status TEXT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
