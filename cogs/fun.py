from discord.ext import commands
from random import choice


class Fun(commands.Cog):

    def __init__(self, data, lang, bot):
        self.data = data
        self.lang = lang
        self.bot = bot

    @commands.command()
    async def piece(self, ctx):
        await ctx.send(f"{ctx.author.mention} :drum: Le résultat est... **{choice(['Pile', 'Face'])}** !")
