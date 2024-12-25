from db import connect_db

def fetch_tournaments_by_type(tournament_type):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM tournaments WHERE type = %s"
    cursor.execute(query, (tournament_type,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    tournaments = fetch_tournaments_by_type("RCO")
    for t in tournaments:
        print(t)
