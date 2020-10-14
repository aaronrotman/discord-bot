# Dependencies
import discord
from config import discord_token
from functions import get_gas_data, get_eth_price

# Instantiate Client to connect to discord
client = discord.Client()

# Event response for when the bot is logged in and ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


# Event response for when the bot receives a message
@client.event 
async def on_message(message):
    
    # Ignore messages sent by this bot
    if message.author == client.user:
        return
    # $hello | Respond with 'Hello!'
    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')
    
    # $gas | Respond with current Ethereum gas price
    elif message.content.lower().startswith('$gas'):
        # Make API call to get eth gas data
        gas_data = get_gas_data()
        # Send the results to the discord channel
        await message.channel.send(f"Safe: {gas_data['safe_gas']}\nPropose: {gas_data['propose_gas']}")
   
    # $eth | Respond with current Ethereum price
    elif message.content.lower().startswith("$eth"):
        # Make API call to get eth price data
        eth_data = get_eth_price()
        # Send the results to the discord channel
        await message.channel.send(f"Ethereum: ${eth_data}")

# Run the app
client.run(discord_token)





