# Dependencies.
import os
import asyncio
from inspect import cleandoc

from dotenv import load_dotenv
import psycopg2
import discord
from discord.ext import commands

from functions import get_gas_data, get_eth_price, query_db_chests

load_dotenv()

# Discord authentication token.
discord_token = os.environ.get("discord_token")

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}", flush=True)
    # Store the channel ID for the bot-commands channel in the Bot Test Zone Discord server.
    channel = bot.get_channel(765448936701427723)
    # Send a message to the channel announcing the bot is ready.
    await channel.send(f"{bot.user.name} at your service.")    


# A simple greeting.
@bot.command(help="A simple greeting")
async def greet(ctx):
    print(f"Greeted user: {ctx.author.name}", flush=True)
    await ctx.send(f"Hello {ctx.author.name} ")


# Post the current price of Ethereum to the channel that sent the command.
@bot.command(help="Ethereum price (USD)")
async def eth(ctx):
    print("Request received: Ethereum Price", flush=True)
    # Make API call to get eth price data.
    eth_data = get_eth_price()
    # Send the results to the discord channel.
    await ctx.channel.send(f"Ethereum Price:\n${eth_data}")


# Post the current gas price for the Ethereum blockchain to the channel that sent the command.
@bot.command(help="Ethereum gas price (gwei)")
async def gas(ctx):
    print("Request received: Ethereum gas price", flush=True)
    # Make API call to get Ethereum gas data.
    gas_data = get_gas_data()
    # Send the results to the discord channel.
    await ctx.channel.send(f"Current gas prices:\nSafe: {gas_data['safe_gas']}\nAverage: {gas_data['propose_gas']}\nFast: {gas_data['fast_gas']}")


# Post the current supply of Gods Unchained chests to the channel that sent the command.
@bot.command(help="GU chest supply data")
async def chests(ctx):
    print('Request received: Chest Supply', flush=True)
    # Query the database for chest supply data.
    chest_data = query_db_chests()
    
    # Send the message to the discord channel.
    chest_message = cleandoc(f"""
        GU Chest Supply
        ------------------------------
        Genesis Rare: {chest_data['genesis_rare']}
        Genesis Legendary: {chest_data['genesis_legendary']}
        TotG Rare: {chest_data['totg_rare']}
        TotG Legendary: {chest_data['totg_legendary']}""")
    await ctx.channel.send(chest_message)


bot.run(discord_token)
