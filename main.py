from discord.ext import commands
import discord
from utils import database, languages, configuration
from cogs import moderation

conf = configuration.Configuration()
data = database.DataBase().save_backup()
lang = languages.Languages().set_lang("fr_FR")

bot = commands.Bot(command_prefix="b!", intents=discord.Intents.all())

bot.add_cog(moderation.Moderation(data, lang, bot))

bot.run(conf.get_token())
