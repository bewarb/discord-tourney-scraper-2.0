from discord_tournament.db import connect_db


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
        print(f"Failed to fetch the table data: {e}")


if __name__ == "__main__":
    # Step 1: Connect to the database
    conn = connect_db()

    # Step 2: If connected, fetch and display the table
    if conn:
        show_table(conn)

        # Close the connection
        conn.close()
        print("\n🔒 Database connection closed.")
