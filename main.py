import discord
from discord.ext import commands, tasks
from scraper import update_database_with_scraper
from db import connect_db
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Define role-to-tournament type mapping
ROLE_TO_TYPE_MAPPING = {
    "M": "M",
    "W": "W",
    "RCO": "RCO",
}

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Required for accessing member roles
intents.message_content = True  # Ensure message content intent is enabled

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Background task to refresh the database every 3 hours
@tasks.loop(hours=1)
async def periodic_scraper():
    print("Running periodic scraper...")
    try:
        update_database_with_scraper()
        print("Database successfully refreshed with the latest tournament data.")
    except Exception as e:
        print(f"Error during periodic scraping: {str(e)}")

@bot.event
async def on_ready():
    """
    Called when the bot is ready.
    Starts the periodic scraper task.
    """
    print(f"Bot is ready. Logged in as {bot.user}")
    periodic_scraper.start()

@bot.command(name="tourney")
async def tourney_command(ctx):
    """
    Fetch and display tournaments based on the user's roles.
    """
    try:
        # Get user roles
        user_roles = [role.name for role in ctx.author.roles]
        allowed_types = [ROLE_TO_TYPE_MAPPING[role] for role in user_roles if role in ROLE_TO_TYPE_MAPPING]

        if not allowed_types:
            await ctx.send("You do not have any roles that match tournament types (M, W, RCO).")
            return

        # Fetch tournaments matching the user's roles
        tournaments = fetch_tournaments_by_roles(allowed_types)

        if not tournaments:
            await ctx.send("No tournaments found that match your roles.")
            return

        message = "**Tournaments Based on Your Roles:**\n"
        for t in tournaments[:10]:  # Show the first 10 tournaments
            message += (
                f"🔹 **Name:** [{t[2]}]({t[3]})\n"
                f"   🔸 **Date:** {t[1]}\n"
                f"   🔸 **Location:** {t[4]}\n"
                f"   🔸 **Max Teams:** {t[8]}\n"
                f"   🔸 **Confirmed Teams:** {t[9]}\n"
                f"   🔸 **Status:** {t[10]}\n\n"
            )
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name="refresh")
async def refresh_command(ctx):
    """
    Manually refresh the database by running the scraper.
    """
    try:
        update_database_with_scraper()
        await ctx.send("Database has been refreshed with the latest tournament data.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

def fetch_tournaments_by_roles(allowed_types):
    """
    Fetch tournaments by allowed types (e.g., M, W, RCO) from the database.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Dynamically build query based on allowed types
    query = f"""
    SELECT * FROM tournaments
    WHERE type IN ({', '.join(['%s'] * len(allowed_types))})
    """
    cursor.execute(query, allowed_types)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@bot.event
async def on_message(message):
    user_roles = [role.name for role in message.author.roles]
    print(f"User: {message.author.name}, Roles: {user_roles}")
    await bot.process_commands(message)


# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
