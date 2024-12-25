from db import connect_db

def insert_tournaments(data):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    INSERT INTO tournaments (date, name, link, location, type, level, cost, max_teams, confirmed, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
if __name__ == "__main__":
    tournaments = [
        ("12/21/24", "RCO C", "https://yankee.org/tournaments/rco-c-12-21-2024", "TUH", "RCO", "C", "$200", 10, 5, "Open"),
        ("01/01/25", "M C", "https://yankee.org/tournaments/m-c-01-01-2025", "BRU", "M", "C", "$150", 8, 6, "Open"),
    ]
    insert_tournaments(tournaments)
    print("Data inserted successfully.")
