from discord.ext import commands
import discord
from utils import database, languages, configuration
from cogs import moderation, roleplay, fun, sending

conf = configuration.Configuration()
data = database.DataBase().save_backup()
lang = languages.Languages().set_lang("fr_FR")

bot = commands.Bot(command_prefix="b!", intents=discord.Intents.all())

bot.add_cog(moderation.Moderation(data, lang, bot))
bot.add_cog(roleplay.RolePlay(data, lang, bot))
bot.add_cog(fun.Fun(data, lang, bot))
bot.add_cog(sending.Sending(data, lang, bot))


@bot.command()
async def report(ctx, *, message):
    data.add_report(ctx.author, message)
    embed = discord.Embed(title="Report Effectué", description="Merci pour votre aide !", color=0x00FF4D)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def reports(ctx):
    embed = discord.Embed(title="Liste des Reports", description=f"Liste des bugs reportés", color=0x8C8D8D)
    for bug_report in data.get_reports():
        embed.add_field(name=f"{bug_report[0]} : Reporté par {bug_report[1]}", value=bug_report[2], inline=False)
    await ctx.send(embed=embed)


bot.run(conf.get_token())
