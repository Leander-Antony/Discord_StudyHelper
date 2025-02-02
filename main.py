import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for tasks
tasks = {}
user_tasks = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()  # Sync the new commands

@bot.tree.command(name='commands', description='Displays all available commands.')
async def commands_list(interaction: discord.Interaction):
    commands_list = [
        "/commands - Displays this help message.",
        "/status - Provides the current status of the project.",
        "/update [text] - Post a project update.",
        "/report [issue] - Submit a report or issue.",
        "/tasks assign [task] [assignee] - Assign a task to a user.",
        "/tasks complete [task] - Mark a task as completed.",
        "/tasks list - List all tasks or your assigned tasks.",
        "/schedule - Displays upcoming meetings and deadlines.",
        "/data - Provides access to project-related data.",
        "/model [status] - Shows or manages the AI model status.",
        "/feedback [message] - Provides feedback or suggestions."
    ]
    await interaction.response.send_message("\n".join(commands_list))

@bot.tree.command(name='status', description='Provides the current status of the project.')
async def status(interaction: discord.Interaction):
    # Placeholder for status
    await interaction.response.send_message("Project status: All systems operational.")

@bot.tree.command(name='update', description='Post a project update.')
@app_commands.describe(text='The update text to post.')
async def update(interaction: discord.Interaction, text: str):
    # Update project status with the provided text
    global current_status
    current_status = text
    await interaction.response.send_message(f"Project status updated to: {text}")

@bot.tree.command(name='report', description='Submit a report or issue.')
@app_commands.describe(issue='The issue to report.')
async def report(interaction: discord.Interaction, issue: str):
    # Ping the server owner with the reported issue
    owner = interaction.guild.owner
    if owner:
        await owner.send(f"Issue reported by {interaction.user}: {issue}")
        await interaction.response.send_message(f"Issue reported and server owner notified: {issue}")
    else:
        await interaction.response.send_message("Server owner not found.")

@bot.tree.command(name='tasks', description='Manage tasks.')
@app_commands.describe(action='Action to perform on tasks', args='Arguments for the action.')
async def tasks_command(interaction: discord.Interaction, action: str = None, args: str = None):
    global tasks, user_tasks
    if action == 'assign':
        try:
            task, assignee = args.rsplit(' ', 1)
            if assignee not in user_tasks:
                user_tasks[assignee] = []
            tasks[task] = assignee
            user_tasks[assignee].append(task)
            await interaction.response.send_message(f"Task '{task}' assigned to {assignee}.")
        except ValueError:
            await interaction.response.send_message("Usage: /tasks assign [task] [assignee]")

    elif action == 'complete':
        if args in tasks:
            assignee = tasks.pop(args)
            user_tasks[assignee].remove(args)
            if not user_tasks[assignee]:
                del user_tasks[assignee]
            await interaction.response.send_message(f"Task '{args}' marked as completed.")
        else:
            await interaction.response.send_message(f"Task '{args}' not found or already completed.")

    elif action == 'list':
        user = interaction.user.name
        if args == 'all':
            if tasks:
                task_list = [f"{task} (Assigned to {assignee})" for task, assignee in tasks.items()]
                await interaction.response.send_message("All tasks:\n" + "\n".join(task_list))
            else:
                await interaction.response.send_message("No tasks available.")
        else:
            assigned_tasks = user_tasks.get(user, [])
            if assigned_tasks:
                await interaction.response.send_message("Your tasks:\n" + "\n".join(assigned_tasks))
            else:
                await interaction.response.send_message("You have no assigned tasks.")

    else:
        await interaction.response.send_message("Usage: /tasks [assign | complete | list]")

@bot.tree.command(name='schedule', description='Displays upcoming meetings and deadlines.')
async def schedule(interaction: discord.Interaction):
    # Placeholder for displaying the schedule
    await interaction.response.send_message("Upcoming schedule: No upcoming meetings.")

@bot.tree.command(name='data', description='Provides access to project-related data.')
async def data(interaction: discord.Interaction):
    # Placeholder for accessing project-related data
    await interaction.response.send_message("Project data: No data available.")

@bot.tree.command(name='model', description='Shows or manages the AI model status.')
@app_commands.describe(status='The model status to set.')
async def model(interaction: discord.Interaction, status: str = None):
    if status:
        # Placeholder for managing model status
        await interaction.response.send_message(f"Model status: {status}")
    else:
        # Placeholder for showing model status
        await interaction.response.send_message("Model status: Operational")

@bot.tree.command(name='feedback', description='Provides feedback or suggestions.')
@app_commands.describe(message='The feedback message.')
async def feedback(interaction: discord.Interaction, message: str):
    # Placeholder for providing feedback
    await interaction.response.send_message(f"Feedback received: {message}")

bot.run(TOKEN)
