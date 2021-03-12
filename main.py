import discord
import os
import pokemoncard
import random
from replit import db # for database
from keep_alive import keep_alive


# import commands
from Commands.card import card


client = discord.Client()

prefix = "c."

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  # client.change_Presence(status=discord.Status.idle, activity=discord.Game("Pokemon Cards"))
  #client.change_Presence(status=)
  game = discord.Game("c.card")
  await client.change_presence(status=discord.Status.online, activity=game)
  pokemoncard.initializeCards()

# on message event
@client.event
async def on_message(message):
  content = message.content.lower();


  
  if(not message.author.bot and content[0:2] == prefix):
    
    content = content.replace(prefix, "", 1)
    if(content.startswith("card")):
      await card(message)
    

keep_alive()
client.run(os.getenv("TOKEN"))