
import discord
import os
import pokemoncard
from db import getTradeList
from keep_alive import keep_alive

# Import commands
from Commands.card import card2
from Commands.collection import collection1
from Commands.trade import trade
from Commands.trade import tradeAccepted
from Commands.trade import tradeDeclined

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


@client.event
async def on_raw_reaction_add(payload):
    print("hi")
    if(payload.user_id!=client.user.id):

        # print(str(payload.emoji.name))

        for pair in getTradeList():
            sendPair = pair[0]
            recPair = pair[1]
            channel = await client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.channel_id == sendPair[0] and payload.message_id == sendPair[1]:
                print("message recognized")
                if payload.emoji.name == '\u274c': # ❌
                    await tradeDeclined(client, message)
            elif payload.channel_id == recPair[0] and payload.message_id == recPair[1]:
                if payload.emoji.name == '\u2705': # ✅
                    await tradeAccepted(client, message)
                elif payload.emoji.name == '\u274c': # ❌
                    await tradeDeclined(client, message)


# On message event
@client.event
async def on_message(message):

  content = message.content.lower();

  if(not message.author.bot and content[0:2] == prefix):

    content = content.replace(prefix, "", 1)
    if content.startswith("card"):
      await card2(message)
    elif content.startswith("col") or content.startswith("collection"):
      await collection1(message)
    elif content.startswith("trade"):
        await trade(message)

  #   commands = {"card":card2(message), "col":collection1(message), "collection":collection1(message), "trade":trade(message)}
  #   if content.split()[0] in commands: commands[conent.split()[0]]


keep_alive()
client.run(os.getenv("TOKEN"))
