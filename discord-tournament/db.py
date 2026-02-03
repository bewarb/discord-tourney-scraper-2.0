import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "discord_tournaments")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")

def connect_db():
    """
    Establish a connection to the PostgreSQL database.
    """
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def initialize_database():
    """
    Create the tournaments table if it doesn't exist.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Create the tournaments table
    create_table_query = '''
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
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
