from discord import utils, Embed
from discord.ext import commands


class RolePlay(commands.Cog):

    def __init__(self, data, lang, bot: commands.Bot):
        self.data = data
        self.lang = lang
        self.bot = bot

    @commands.command()
    async def rp(self, ctx, receiver, *, text):
        try:
            member_receiver = utils.get(ctx.guild.members, id=int(receiver.replace("<", "").replace(">", "").replace("@", "").replace("!", "")))
        except ValueError:
            member_receiver = None
        if member_receiver is not None:
            embed = Embed(title=str(ctx.author), color=0x25D7BF)
            embed.add_field(name=f"S'adresse à **{(member_receiver, receiver)[member_receiver is None]}**", value=text)
            await ctx.message.delete()
            await ctx.send(embed=embed)

    @commands.command()
    async def rpa(self, ctx, *, action: str):
        embed = Embed(title=str(ctx.author), color=0x035348)
        embed.add_field(name="Exécute une **action**", value="_" + action + "_")
        await ctx.message.delete()
        await ctx.send(embed=embed)
