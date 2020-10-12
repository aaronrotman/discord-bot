# Dependencies
import discord
from config import discord_token

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
    # Respond to messages that start with '$hello '
    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')
    # Test response
    elif message.content.lower().startswith('$test'):
        await message.channel.send("Testing...testing...1...2...3")

# Run the app
client.run(discord_token)





