import random
import discord
from replit import db
from user import updateRolls
from user import collectionAdd
from datetime import datetime
import pokemoncard

def getCard(): 
  rand = random.randint(1, 27)
  cardType = ""
  if(rand<15): cardType="common"
  elif(rand<24): cardType="uncommon"
  elif(rand<26): cardType="rare"
  else: cardType="rare holo"

  # cardVar = random.choice(pokemoncard.cardsByRarity.get(cardType)) # replacing with new usage
  
  cardVar = random.choice(pokemoncard.byRarity(cardType))
  return cardVar

def embedCard(author, cardVar):
  title = ""

  if cardVar.rarity.lower() == "rare holo": title = "You unpacked a Holo Rare "+cardVar.name+"!"
  else: title = "You unpacked a "+cardVar.name+"!"

  embedVar = discord.Embed(title=title)
  embedVar.set_image(url=cardVar.imgurl)
  embedVar.set_author(name=author.display_name, icon_url=author.avatar_url)

  return embedVar

async def card(message):
  await message.channel.send(embed=embedCard(author=message.author, cardVar = getCard()))


async def card1(message): # building so that it will save and also limit rolls
  
  rolls = updateRolls(message.author, datetime.today())
  if rolls != 0:
    card = getCard()
    collectionAdd(db[message.author.id], card)
    await message.channel.send(embed=embedCard(cardVar=card))
    db[message.author.id].rolls -= 1
  else:
    await message.channel.send(message="You cannot do this command")

  await message.channel.send("You have "+rolls+"rolls left.")
