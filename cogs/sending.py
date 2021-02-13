import discord
from discord.ext import commands


class Sending(commands.Cog):

    def __init__(self, data, lang, bot):
        self.data = data
        self.lang = lang
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendPrivate(self, ctx, member: discord.Member, *, message):
        embed = discord.Embed(title="Message Reçu", description=f"Du serveur `{ctx.guild}`", color=0x7F8553)
        embed.add_field(name="Message", value=message)
        embed.set_footer(text=self.lang.get_path("content_warning"))
        await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendChannel(self, ctx, member: discord.TextChannel, *, message):
        embed = discord.Embed(title="Message Reçu", description=f"De `{ctx.author}`", color=0x7F8553)
        embed.add_field(name="Message", value=message)
        embed.set_footer(text=self.lang.get_path("content_warning"))
        await member.send(embed=embed)

    @sendPrivate.error
    @sendChannel.error
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed.add_field(name="Raison", value="Il vous manque des permissions pour faire ceci !", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            embed.add_field(name="Raison", value="Le membre que vous avez choisi n'existe pas...", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.ChannelNotFound):
            embed.add_field(name="Raison", value="Le salon que vous avez choisi n'existe pas...", inline=False)
            await ctx.send(embed=embed)
