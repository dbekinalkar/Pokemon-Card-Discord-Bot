import random
import discord
import pokemoncard

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


async def card(message):
  
      await message.channel.send(embed=embedCard(message=message, cardVar=getCard()))
