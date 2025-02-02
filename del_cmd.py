import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # Fetch all global commands
    commands = await bot.tree.fetch_commands()
    
    # Delete each command
    for command in commands:
        await bot.tree.delete_command(command.id)
    
    # Sync new commands
    await bot.tree.sync()
    print("Old commands deleted and new commands synced.")

bot.run(TOKEN)
