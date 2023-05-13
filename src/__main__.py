import discord
import os
import logging
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


client.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)
