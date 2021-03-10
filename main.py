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
  pokemoncard.initializeCards()

# Command functions

def getCard(): 
  rand = random.randint(1, 27)
  cardType = ""
  if(rand<15): cardType="common"
  elif(rand<24): cardType="uncommon"
  elif(rand<26): cardType="rare"
  else: cardType="rare holo"
  cardVar = random.choice(pokemoncard.cards.get(cardType))
  return cardVar

def embedCard(message, cardVar):
  title = ""

  if cardVar.rarity.lower() == "rare holo": title = "You unpacked a Holo Rare "+cardVar.name+"!"
  else: title = "You unpacked a "+cardVar.name+"!"

  embedVar = discord.Embed(title=title)
  embedVar.set_image(url=cardVar.imgurl)
  return embedVar

# on message event
@client.event
async def on_message(message):
  if(not message.author.bot and message.content.startswith(prefix)):
    content = message.content.replace(prefix,"",1)
    if(content.startswith("card")):
      await card(message)
    

keep_alive()
client.run(os.getenv("TOKEN"))

