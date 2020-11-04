# Dependencies
import os

import discord
from dotenv import load_dotenv
import psycopg2
import asyncio

from functions import get_gas_data, get_eth_price
from database_functions import update_db_chests

# Load environment variables
load_dotenv()

# Database url
database_url = os.environ.get("DATABASE_URL")

# Discord authentication token
discord_token = os.environ.get('discord_token')

# Instantiate Client to connect to discord
client = discord.Client()

# Event response for when the bot is logged in and ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Store the channel ID for the bot-commands channel in the Bot Test Zone Discord server
    channel = client.get_channel(765448936701427723)
    # Send a message to the channel announcing the bot is ready
    await channel.send(f"{client.user.name} is up and running!")
    
    # Update the database table 'gu_chests' every 10 minutes
    while True:
        # Update the database table 'gu_chests'
        update_db_chests()
        # Wait 10 minutes before the next update
        await asyncio.sleep(1 * 60 * 10 )

# Event response for when the bot receives a message
@client.event 
async def on_message(message):
    
    # Ignore messages sent by this bot
    if message.author == client.user:
        return

    # $hello | Respond with 'Hello!'
    if message.content.lower().startswith('$hello'):
        await message.channel.send(f"Hello {message.author.name}")
    
    # $gas | Respond with current Ethereum gas price
    elif message.content.lower().startswith('$gas'):
        # Make API call to get Ethereum gas data
        gas_data = get_gas_data()
        # Send the results to the discord channel
        await message.channel.send(f"Current gas prices:\nSafe: {gas_data['safe_gas']}\nPropose: {gas_data['propose_gas']}\nFast: {gas_data['fast_gas']}")
   
    # $eth | Respond with current Ethereum price
    elif message.content.lower().startswith("$eth"):
        # Make API call to get eth price data
        eth_data = get_eth_price()
        # Send the results to the discord channel
        await message.channel.send(f"Ethereum Price:\n${eth_data}")

    # $chest | Respond with current total supply data for Gods Unchained Chests
    elif message.content.lower().startswith("$chest"):
        try:
            # Connect to the database
            conn = psycopg2.connect(database_url, sslmode='require')
            cur = conn.cursor()
        
            # Query the database
            cur.execute("""
                SELECT *
                FROM gu_chests
                ORDER BY id;"""
            )
            
            # Store the queried data     
            data = cur.fetchall()
        
            # Send the results to the discord channel
            await message.channel.send(
                "GU Chest Supply:\n"
                "-------------------------\n"
                f"Genesis Rare: {data[0][3]}\n"
                f"Genesis Legendary: {data[1][3]}\n"
                f"TotG Rare: {data[2][3]}\n"
                f"TotG Legendary: {data[3][3]}\n"
            )

            # Close connections with the database
            cur.close()
            conn.close()

        except Exception as e:
            print(e)
            await message.channel.send("Database connection failed.")



# Run the app
client.run(discord_token)
