import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials from .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "discord_tournaments")
DB_USER = os.getenv("DB_USER", "discord_user")
DB_PASS = os.getenv("DB_PASS", "your_password")

def connect_to_db():
    """
    Connect to the PostgreSQL database and return the connection.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Successfully connected to the database.")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")
        return None

def show_table(conn):
    """
    Fetch and display the contents of the 'tournaments' table.
    """
    try:
        # Create a cursor
        cursor = conn.cursor()

        # Execute the query to fetch the table
        query = "SELECT * FROM tournaments;"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Display the table contents
        print("\nContents of the 'tournaments' table:")
        for row in rows:
            print(row)

        # Close the cursor
        cursor.close()
    except Exception as e:
        print(f"❌ Failed to fetch the table data: {e}")

if __name__ == "__main__":
    # Step 1: Connect to the database
    conn = connect_to_db()

    # Step 2: If connected, fetch and display the table
    if conn:
        show_table(conn)

        # Close the connection
        conn.close()
        print("\n🔒 Database connection closed.")
