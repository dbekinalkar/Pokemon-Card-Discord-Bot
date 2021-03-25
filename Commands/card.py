import random
import discord

from db import freePacks2
from db import updatePacks
from db import getPacks
from db import addToCollection
from db import getTimeLeft
import time
import pokemoncard

def getCard(): # Not Used
  rand = random.randint(1, 27)
  cardType = ""
  if(rand<15): cardType="common"
  elif(rand<24): cardType="uncommon"
  elif(rand<26): cardType="rare"
  else: cardType="rare holo"

  # cardVar = random.choice(pokemoncard.cardsByRarity.get(cardType)) # replacing with new usage
  
  cardVar = random.choice(pokemoncard.byRarity(pokemoncard.cards, cardType))
  return cardVar

def embedCard(author, cardVar): # Not Used
  title = ""

  if cardVar.rarity.lower() == "rare holo": title = "You unpacked a Holo Rare "+cardVar.name+"!"
  else: title = "You unpacked a "+cardVar.name+"!"

  embedVar = discord.Embed(title=title)
  embedVar.set_image(url=cardVar.imgurl)
  embedVar.set_author(name=author.display_name, icon_url=author.avatar_url)

  return embedVar

async def card(message): # Not Used
  await message.channel.send(embed=embedCard(author=message.author, cardVar = getCard()))


async def card2(message):

  freePacks2(message.author.id, time.time()) # Update with free packs

  if getPacks(message.author.id) > 0:
    updatePacks(message.author.id, int(-1)) # Use 1 pack
    
    # Get a card

    rand = random.randint(1, 27)
    cardType = ""
    if(rand<15): cardType="common"
    elif(rand<24): cardType="uncommon"
    elif(rand<26): cardType="rare"
    else: cardType="rare holo"

    card = random.choice(pokemoncard.byRarity(pokemoncard.cards, cardType))


    addToCollection(message.author.id, card) # Add card to collection


    # Build embed and send
    title = ""

    if card.rarity.lower() == "rare holo": 
      title = "You unpacked a Holo Rare "+card.name+"!"
    else: title = "You unpacked a "+card.name+"!"

    embedVar = discord.Embed(title=title)
    embedVar.set_image(url=card.imgurl)
    embedVar.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embedVar.set_footer(text="You have "+str(int(getPacks(message.author.id)))+" packs left.")

    
    await message.channel.send(embed=embedVar)

  else:
    await message.channel.send("<@"+str(message.author.id)+"> Wait "+str(int(getTimeLeft(message.author.id, time.time())//60))+" minutes"
    +"\nYou have "+str(int(getPacks(message.author.id)))+" packs left.")

  # await message.channel.send("<@"+str(message.author.id)+"> You have "+str(int(getPacks(message.author.id)))+" packs left.")