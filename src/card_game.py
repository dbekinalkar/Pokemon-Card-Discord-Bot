import discord
from discord.ext import commands

class CardGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def card(self, ctx):
        pass

    @commands.command()
    async def inventory(self, ctx):
        pass

    async def trade(self, ctx, member: discord.Member = None, to_give: dict[str] = None, to_get: dict[str] = None):
        pass