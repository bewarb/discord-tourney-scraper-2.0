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

def fetch_tournaments(allowed_types=None, level_filter=None, location_filter=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM tournaments WHERE 1=1"
    params = []

    if allowed_types:
        query += " AND type IN (%s)" % ", ".join(["%s"] * len(allowed_types))
        params.extend(allowed_types)

    if level_filter:
        query += " AND level = %s"
        params.append(level_filter)

    if location_filter:
        query += " AND location ILIKE %s"
        params.append(f"%{location_filter}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    tournaments = fetch_tournaments_by_type("RCO")
    for t in tournaments:
        print(t)
