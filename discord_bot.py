# Dependencies
import discord
from functions import get_gas_data, get_eth_price
import os
from dotenv import load_dotenv

load_dotenv()

# Import Discord token from environment variables
discord_token = os.environ.get('discord_token')

# Instantiate Client to connect to discord
client = discord.Client()

# Event response for when the bot is logged in and ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Store the channel ID for the bot-commands channel in the Bot Test Zone Discord server
    channel = client.get_channel("765448936701427723")
    # Send a message to the channel announcing the bot is ready
    await channel.send(f"Ether Bot is up and running!")

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
        # Make API call to get eth gas data
        gas_data = get_gas_data()
        # Send the results to the discord channel
        await message.channel.send(f"Current gas prices:\nSafe: {gas_data['safe_gas']}\nPropose: {gas_data['propose_gas']}\nFast: {gas_data['fast_gas']}")
   
    # $eth | Respond with current Ethereum price
    elif message.content.lower().startswith("$eth"):
        # Make API call to get eth price data
        eth_data = get_eth_price()
        # Send the results to the discord channel
        await message.channel.send(f"Ethereum Price:\n${eth_data}")

# Run the app
client.run(discord_token)