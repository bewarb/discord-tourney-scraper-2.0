import os

import discord
from db import connect_db
from discord.ext import commands, tasks
from dotenv import load_dotenv
from scraper import update_database_with_scraper
from fetch_data import fetch_tournaments


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
@tasks.loop(hours=3)
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
async def tourney_command(ctx, *args):
    """
    Fetch and display tournaments based on the user's roles or provided filters.
    """
    try:
        # Default to user roles if no arguments provided
        user_roles = [role.name for role in ctx.author.roles]
        allowed_types = [
            ROLE_TO_TYPE_MAPPING[role] for role in user_roles if role in ROLE_TO_TYPE_MAPPING
        ]

        # Parse arguments
        type_filter = (
            args[0] if len(args) > 0 and args[0] in ROLE_TO_TYPE_MAPPING.values() else None
        )
        level_filter = args[1] if len(args) > 1 else None
        location_filter = args[2] if len(args) > 2 else None

        # Fetch tournaments based on filters or roles
        if args:  # If filters are provided
            tournaments = fetch_tournaments(
                allowed_types=[type_filter] if type_filter else None,
                level_filter=level_filter,
                location_filter=location_filter,
            )
        else:  # Default to roles
            tournaments = fetch_tournaments(allowed_types=allowed_types)

        # Handle no results
        if not tournaments:
            await ctx.send("No tournaments found matching your criteria.")
            return

        # Format and send results
        message = "**Tournaments:**\n"
        for t in tournaments[:5]:
            message += (
                f"\ud83d\udd39 **Name:** [{t[2]}]({t[3]})\n"
                f"   \ud83d\udd38 **Date:** {t[1]}\n"
                f"   \ud83d\udd38 **Location:** {t[4]}\n"
                f"   \ud83d\udd38 **Type:** {t[5]}\n"
                f"   \ud83d\udd38 **Level:** {t[6]}\n"
                f"   \ud83d\udd38 **Max Teams:** {t[8]}\n"
                f"   \ud83d\udd38 **Confirmed Teams:** {t[9]}\n"
                f"   \ud83d\udd38 **Status:** {t[10]}\n\n"
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

@bot.event
async def on_message(message):
    user_roles = [role.name for role in message.author.roles]
    print(f"User: {message.author.name}, Roles: {user_roles}")
    await bot.process_commands(message)


# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
