# discord-tourney-scraper-2.0

## Overview

The Discord Tournament Scraper is a Python-based project that integrates with Discord to scrape and display volleyball tournament information from the Yankee website. It fetches tournament data, stores it in a PostgreSQL database, and provides Discord commands for users to filter and view tournaments based on their roles.

### Project Structure

1. Core Files

* main.py 

The main bot script that interacts with Discord.

Handles commands like !tourney to fetch and display tournaments based on user roles.

Periodically updates the tournament database using the scraper.

Features:

Command filtering based on roles (M, W, RCO).

Background task to refresh data every 3 hours.

scraper.py

Scrapes the Yankee tournaments webpage to extract tournament data (e.g., name, date, location, status).

Cleans and stores the data in a PostgreSQL database.

Handles edge cases like missing fields or unavailable links.

db.py

Manages the PostgreSQL database connection.

Provides a reusable connect_db function for all database operations.

fetch_data.py

Contains functions to query the database for specific filters (e.g., type, location, date).

Modularized for easy integration and customization.

Examples:

Fetch tournaments by type (fetch_tournaments_by_type).

Fetch tournaments by multiple criteria.

insert_data.py

A utility script for manually inserting example data into the database.

Useful for testing or initializing the database.

Setup Instructions

1. Prerequisites

Python (3.11 or compatible version)

PostgreSQL installed locally

Required Python libraries (listed in requirements.txt):

pip install -r requirements.txt

Environment VariablesCreate a .env file with the following variables:

DISCORD_TOKEN=<your_discord_bot_token>
DB_HOST=localhost
DB_NAME=discord_tournaments
DB_USER=admin
DB_PASS=<your_password>

2. Database Setup

Access PostgreSQL:

psql -U <your_db_user>

Create Database and User:

CREATE DATABASE discord_tournaments;
CREATE USER admin WITH PASSWORD '<your_password>';

Grant Permissions:

GRANT ALL PRIVILEGES ON DATABASE discord_tournaments TO admin;
\c discord_tournaments
GRANT USAGE, SELECT, UPDATE ON SEQUENCE tournaments_id_seq TO admin;
GRANT INSERT, SELECT, DELETE, UPDATE ON tournaments TO admin;

Create the Table:Run the following SQL command:

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

3. Run the Project

A. Run the Scraper

Populates the database with tournament data:

python scraper.py

B. Start the Bot

Runs the Discord bot to listen for commands:

python main.py

Key Features

Discord Integration:

Commands:

!tourney: Displays tournaments based on the user's assigned roles.

!refresh: Manually refreshes tournament data.

Database Management:

Stores tournament data for efficient querying.

Allows filtering based on type, location, or other criteria.

Web Scraping:

Extracts data from the Yankee tournament site dynamically.

Handles website structure changes gracefully.

Future Enhancements: Docker & Raspberry Pi Integration

Why Docker?

Simplifies setup by containerizing the project.

Ensures consistency across different environments.

Easier deployment on lightweight devices like Raspberry Pi.

Plan

Dockerize the Application:

Create a Dockerfile to set up the Python environment and install dependencies.

Use docker-compose to orchestrate the bot, scraper, and PostgreSQL database.

Deploy on Raspberry Pi:

Build the Docker image for ARM architecture.

Schedule periodic scraping and ensure the bot runs continuously.

Streamline Updates:

Auto-restart the bot if it crashes.

Implement health checks for the scraper and database.

Contribution

Feel free to fork this repository and submit pull requests for any improvements or features you’d like to add. For any issues or questions, open a GitHub issue.

Happy Scraping! 🚀

