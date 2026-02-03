import requests
from bs4 import BeautifulSoup
from db import connect_db

BASE_URL = "https://yankee.org/tournaments"  # Replace with the actual URL


def scrape_tournaments():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    tournaments = []

    # Locate the table body containing tournament rows
    table_body = soup.find("tbody")  # Adjusted to the <tbody> element
    if not table_body:
        print("No table body found. Check the website structure.")
        return tournaments

    rows = table_body.find_all("tr")  # Find all table rows
    for row in rows:
        try:
            # Extract data safely
            date = row.find_all("td")[0].text.strip()  # Date
            name_cell = row.find_all("td")[1]  # Tournament name and link
            name = name_cell.text.strip()
            link = name_cell.find("a")["href"] if name_cell.find("a") else "No link available"
            location = row.find_all("td")[2].text.strip()  # Location
            type_ = row.find_all("td")[3].text.strip()  # Type
            level = row.find_all("td")[4].text.strip()  # Level
            cost = row.find_all("td")[7].text.strip()  # Cost
            max_teams = row.find_all("td")[9].text.strip()  # Max teams
            confirmed = row.find_all("td")[10].text.strip().split()[0]  # Confirmed teams
            status = row.find_all("td")[11].text.strip()  # Status

            # Add the tournament to the list
            tournaments.append(
                {
                    "date": date,
                    "name": name,
                    "link": link,
                    "location": location,
                    "type": type_,
                    "level": level,
                    "cost": cost,
                    "max_teams": int(max_teams),
                    "confirmed": int(confirmed),
                    "status": status,
                }
            )
        except Exception as e:
            print(f"Error parsing row: {e}")

    return tournaments


def update_database_with_scraper():
    """
    Scrape tournament data and update the database.
    """
    tournaments = scrape_tournaments()
    if not tournaments:
        print("No tournaments found to insert.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Clear the table before inserting new data
    try:
        cursor.execute("DELETE FROM tournaments")
        print("Cleared the tournaments table.")
    except Exception as e:
        print(f"Error clearing table: {e}")

    # Insert the scraped data into the table
    for t in tournaments:
        try:
            cursor.execute(
                """
                INSERT INTO tournaments (date, name, link, location, type, level, cost, max_teams, confirmed, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    t["date"],
                    t["name"],
                    t["link"],
                    t["location"],
                    t["type"],
                    t["level"],
                    t["cost"],
                    t["max_teams"],
                    t["confirmed"],
                    t["status"],
                ),
            )
            print(f"Inserted: {t['name']}")
        except Exception as e:
            print(f"Error inserting {t['name']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database updated successfully.")


if __name__ == "__main__":
    update_database_with_scraper()
