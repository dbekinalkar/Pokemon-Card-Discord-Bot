# Check out this last line of code
# Ensure that running 'c.card' multiple times does not decrease time for next card
# db.py



import discord
import os
import pokemoncard
from keep_alive import keep_alive
from replit import db

# Import commands
from Commands.card import card2
from Commands.collection import collection1

# Global Variables
client = discord.Client()
prefix = "c."

# Starting the bot
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  game = discord.Game("c.card")
  await client.change_presence(status=discord.Status.online, activity=game)
  pokemoncard.initializeCards()
  # del db["381953351186907139t"] # TESTING: DELETE

# On message event
@client.event
async def on_message(message):
  content = message.content.lower();
  
  if(not message.author.bot and content[0:2] == prefix):
    
    content = content.replace(prefix, "", 1)
    if(content.startswith("card")):
      # await card(message)
      await card2(message)
    elif content.startswith("col") or content.startswith("collection"):
      await collection1(message)


keep_alive()
client.run(os.getenv("TOKEN"))