# Dependencies
import os

import discord
from dotenv import load_dotenv
import psycopg2
import asyncio
from discord.ext import commands

load_dotenv()

# Discord authentication token
discord_token = os.environ.get('discord_token')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Store the channel ID for the bot-commands channel in the Bot Test Zone Discord server
    channel = bot.get_channel(765448936701427723)
    # Send a message to the channel announcing the bot is ready
    await channel.send(f"{bot.user.name} is up and running!")    

# A simple greeting 
@bot.command()
async def greet(ctx):
    print(f"Greeted user: {ctx.author.name}")
    await ctx.send(f"Hello {ctx.author.name} ")



bot.run(discord_token)
