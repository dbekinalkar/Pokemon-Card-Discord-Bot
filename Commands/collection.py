import discord
import db
import pokemoncard
from pokemoncard import getCard
from pokemoncard import byRarity

async def collection(message):

  col = db.getCollection(message.author.id)


  embed = discord.Embed(title="Collection")
  embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)

  if col=={}:
    embed.add_field(name="Hi!", value="Try opening some packs using 'c.card'")
  else:
    for key in col.keys():
      embed.add_field(name=key, value = col[key])

  await message.channel.send(embed=embed)


async def collection1(message):
  col = db.getCollection(message.author.id)


  embed = discord.Embed(title="Collection") # Building blank embed
  embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)


  cardCol = []  # Creating new list with Card Objects
  for cardName in col:
    cardCol.append(getCard(cardName))


  for rarity in pokemoncard.rarities:
    colByRarity = byRarity(cardCol, rarity) # Finding the cards of only this rarity

    if len(colByRarity) > 0:
      fieldName="["+pokemoncard.rarities[rarity]+"] "+rarity.title()
      value=""
      for card in colByRarity:
        value+=card.name + " [x"+str(col[card.name])+"]\n"

      embed.add_field(name = fieldName, value = value)

  await message.channel.send(embed=embed)
