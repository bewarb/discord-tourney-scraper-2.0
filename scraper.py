from bs4 import BeautifulSoup
import requests
from db import connect_db

BASE_URL = 'https://yankee.org'

def scrape_tournaments():
    """
    Scrape tournaments from the website and return them as a list of dictionaries.
    """
    response = requests.get(f"{BASE_URL}/tournaments")
    response.raise_for_status()  # Raise an error if the request fails
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the tournament table
    table = soup.find("table", class_="tournamentList")
    tournaments = []

    for row in table.find("tbody").find_all("tr"):
        try:
            cells = row.find_all("td")
            tournaments.append({
                "date": cells[0].text.strip(),
                "name": cells[1].text.strip(),
                "link": BASE_URL + row["data-url"],
                "location": cells[2].text.strip(),
                "type": cells[3].text.strip(),
                "level": cells[4].text.strip(),
                "cost": cells[7].text.strip(),
                "max_teams": int(cells[9].text.strip()),
                "confirmed": int(cells[10].text.strip()),
                "status": cells[11].text.strip()
            })
        except (AttributeError, IndexError, ValueError):
            # Skip rows with missing or invalid data
            continue

    return tournaments

def update_database_with_scraper():
    """
    Scrape tournaments and update the database with fresh data.
    """
    tournaments = scrape_tournaments()
    conn = connect_db()
    cursor = conn.cursor()

    # Clear existing data (optional: depends on your requirements)
    cursor.execute("DELETE FROM tournaments")

    # Insert new data
    insert_query = '''
    INSERT INTO tournaments (date, name, link, location, type, level, cost, max_teams, confirmed, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    tournament_data = [
        (t["date"], t["name"], t["link"], t["location"], t["type"], t["level"], t["cost"], t["max_teams"], t["confirmed"], t["status"])
        for t in tournaments
    ]
    cursor.executemany(insert_query, tournament_data)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database updated with scraped data.")

if __name__ == "__main__":
    update_database_with_scraper()
