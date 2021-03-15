import discord
import db

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