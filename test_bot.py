# Dependencies
import os
import asyncio

from dotenv import load_dotenv
import psycopg2
import discord
from discord.ext import commands

from functions import get_gas_data, get_eth_price

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

# Post the current price of Ethereum to the channel that sent the command
@bot.command()
async def eth(ctx):
        print("Request received: Ethereum Price")
        # Make API call to get eth price data
        eth_data = get_eth_price()
        # Send the results to the discord channel
        await ctx.channel.send(f"Ethereum Price:\n${eth_data}")

# Post the current gas price for the Ethereum blockchain to the channel that sent the command
@bot.command()
async def gas(ctx):
        print("Request received: Ethereum gas price")
        # Make API call to get Ethereum gas data
        gas_data = get_gas_data()
        # Send the results to the discord channel
        await ctx.channel.send(f"Current gas prices:\nSafe: {gas_data['safe_gas']}\nAverage: {gas_data['propose_gas']}\nFast: {gas_data['fast_gas']}")



bot.run(discord_token)
