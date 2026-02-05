# discord-tourney-scraper-2.0

A Discord bot that scrapes volleyball tournament data from the Yankee website, stores it in PostgreSQL, and lets Discord users query tournaments based on their roles.

---

## Overview

The **Discord Tournament Scraper** is a Python-based application that:

- Scrapes volleyball tournament data from the Yankee website  
- Stores structured tournament data in a PostgreSQL database  
- Exposes Discord commands to filter and view tournaments  
- Automatically refreshes data on a schedule  

It’s designed to be extensible, deployable, and eventually containerized.

---

## Project Structure

```text
discord_tournament/
├── main.py              # Discord bot entry point
├── scraper.py           # Web scraping + DB update logic
├── db.py                # Database connection + initialization
├── fetch_data.py        # Query helpers for filtering tournaments
├── scripts/
│   ├── insert_data.py   # Insert sample data (testing)
│   └── view_table.py    # Debug: print DB contents
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Core Files

#### `main.py`
- Runs the Discord bot  
- Handles commands like `!tourney` and `!refresh`  
- Filters tournaments based on user roles (M, W, RCO)  
- Periodically refreshes tournament data (every 3 hours)

#### `scraper.py`
- Scrapes the Yankee tournaments webpage  
- Extracts tournament metadata (date, name, location, status, etc.)  
- Inserts cleaned data into PostgreSQL  
- Handles missing fields and malformed rows

#### `db.py`
- Centralized PostgreSQL connection logic  
- Loads required environment variables  
- Initializes the `tournaments` table if needed

#### `fetch_data.py`
- Provides reusable query helpers  
- Supports filtering by:
  - tournament type
  - level
  - location
  - combinations of criteria

#### Utility Scripts (`scripts/`)
- `insert_data.py` – insert example data for testing  
- `view_table.py` – print all tournaments in the database  

---

##  Setup Instructions

### 1 Prerequisites

- **Python 3.11+**
- **PostgreSQL**
- **pip**

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

### 2 Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token
DB_HOST=localhost
DB_NAME=discord_tournaments
DB_USER=admin
DB_PASS=your_password
```

> ⚠️ Do **not** commit `.env` files. Use `.env.example` for sharing config structure.

---

### 3 Database Setup

Access PostgreSQL:

```bash
psql -U <your_db_user>
```

Create database and user:

```sql
CREATE DATABASE discord_tournaments;
CREATE USER admin WITH PASSWORD '<your_password>';
```

Grant permissions:

```sql
GRANT ALL PRIVILEGES ON DATABASE discord_tournaments TO admin;
\c discord_tournaments
GRANT USAGE, SELECT, UPDATE ON SEQUENCE tournaments_id_seq TO admin;
GRANT INSERT, SELECT, DELETE, UPDATE ON tournaments TO admin;
```

Create the tournaments table:

```sql
CREATE TABLE tournaments (
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
);
```

---

##  Running the Project

### A) Run the Scraper (populate DB)

```bash
python -m discord_tournament.scraper
```

### B) Start the Discord Bot

```bash
python -m discord_tournament.main
```

---

##  Discord Commands

### `!tourney`
Displays tournaments filtered by the user’s Discord roles.

Supported role filters:
- `M` – Men’s  
- `W` – Women’s  
- `RCO` – Recreational Co-ed  

Optional arguments:

```text
!tourney <type> <level> <location>
```

### `!refresh`
Manually triggers a database refresh by re-running the scraper.

---

##  Key Features

### Discord Integration
- Role-based filtering  
- Clean formatted output  
- Manual and automatic refresh options  

### Database Management
- Persistent storage via PostgreSQL  
- Efficient querying and filtering  
- Centralized DB access logic  

### Web Scraping
- Dynamic extraction from the Yankee website  
- Defensive parsing against malformed data  
- Easy to adapt if site structure changes  

---

##  Future Enhancements

### Docker & Raspberry Pi Deployment

**Why Docker?**
- Simplifies setup across machines  
- Ensures consistent environments  
- Ideal for lightweight deployment (Raspberry Pi)

**Planned Improvements**
- Dockerfile + docker-compose  
- PostgreSQL container integration  
- ARM builds for Raspberry Pi  
- Health checks + auto-restart  
- Scheduled scraping jobs  

---

##  Contributing

Contributions are welcome!

- Fork the repository  
- Create a feature branch  
- Submit a pull request  

For bugs or questions, please open a GitHub issue.

---

##  Final Notes

This project is actively evolving and designed with extensibility in mind.  
Whether you’re contributing features, improving data quality, or deploying it somewhere fun — welcome aboard.

**Happy Scraping! **
