from discord.ext import commands
import discord


class Moderation(commands.Cog):

    def __init__(self, data, lang, bot: commands.Bot):
        self.data = data
        self.lang = lang
        self.bot = bot

    async def sanction_possible(self, ctx, target: discord.Member):
        if ctx.author.top_role.position < target.top_role.position or ctx.guild.owner_id == target.id:
            embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
            embed.add_field(name="Raison", value="Vous ne pouvez pas sanctionner cette personne.", inline=False)
            await ctx.send(embed=embed)
            return False
        member_bot = discord.utils.get(ctx.guild.members, id=self.bot.user.id)
        if member_bot.top_role.position < target.top_role.position:
            embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
            embed.add_field(name="Raison", value="Le bot ne peut pas sanctionner cette personne.", inline=False)
            await ctx.send(embed=embed)
            return False
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, discord.DMChannel):
                pass
            else:
                for sentence in self.data.get_banwords(message.guild.id):
                    if message.content.lower().find(sentence.lower()) != -1:
                        await message.delete()

    @commands.Cog.listener()
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
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed.add_field(name="Raison", value="Il manque un argument dans la commande !", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addBanword(self, ctx, *, banword):
        self.data.add_banword(ctx.guild.id, banword)

        embed = discord.Embed(title="BanWord Ajouté", description="Vous avez ajouté un banword", color=0x00FF4D)
        embed.add_field(name="BanWord", value=banword, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeBanword(self, ctx, *, banword):
        if self.data.remove_banword(ctx.guild.id, banword):
            embed = discord.Embed(title="BanWord Retiré", description="Vous avez retiré un banword", color=0x00FF4D)
            embed.add_field(name="BanWord", value=banword, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
            embed.add_field(name="Raison", value="Ce banword n'existe pas !", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def getBanwords(self, ctx):
        embed = discord.Embed(title="Liste des BanWords", description=f"Liste des BanWords de {ctx.guild}", color=0x8C8D8D)
        embed_value = ""
        for banword in self.data.get_banwords(ctx.guild.id):
            embed_value = embed_value + " \n- " + banword
        if embed_value != "":
            embed.add_field(name="BanWords trouvés :", value=embed_value)
        else:
            embed.add_field(name="BanWords trouvés :", value="Aucun BanWord trouvé...")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def offenses(self, ctx, user: discord.User):
        embed = discord.Embed(title="Liste des Infractions", description=f"Liste d'infractions de **{str(user)}**", color=0x8C8D8D)
        offenses = 0
        for offense in self.data.get_offenses(ctx.guild.id, user.id):
            offenses += 1
            if offense[4] == 0:
                offense_type = "Avertissement"
            elif offense[4] == 1:
                offense_type = "Mute"
            elif offense[4] == 2:
                offense_type = "Expulsion"
            else:
                offense_type = "Bannissement"
            embed.add_field(name=f"**{offense[2]}** {offense_type}", value=f"Raison : {offense[5]}", inline=False)
        if offenses == 0:
            embed.add_field(name="Aucune infraction", value="Le membre n'a pas d'infractions")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison fournie"):

        if not await self.sanction_possible(ctx, member): return

        self.data.add_offense(ctx.guild.id, member.id, 0, 0, reason)

        embed = discord.Embed(title="Avertissement Reçu", description="Vous avez reçu un avertissement", color=0x00FF4D)
        embed.add_field(name="Serveur", value=str(ctx.guild), inline=False)
        embed.add_field(name="Raison", value=reason)
        await member.send(embed=embed)

        embed = discord.Embed(title="Avertissement Effectué", description="Vous avez averti un membre", color=0x00FF4D)
        embed.add_field(name="Utilisateur", value=str(member), inline=False)
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True, mute_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison fournie"):

        if not await self.sanction_possible(ctx, member): return

        self.data.add_offense(ctx.guild.id, member.id, 1, 0, reason)

        embed = discord.Embed(title="Commande Indisponible", description="Cette commande est indisponible", color=0xFF0020)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison fournie"):

        if not await self.sanction_possible(ctx, member): return

        await member.send(f"{member.mention} Vous avez été expulsé du serveur **{ctx.guild}** !")
        await member.kick(reason=reason)

        self.data.add_offense(ctx.guild.id, member.id, 2, 3, reason)

        embed = discord.Embed(title="Expulsion Effectuée", description="Vous avez expulsé un membre", color=0x00FF4D)
        embed.add_field(name="Utilisateur", value=str(member), inline=False)
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison fournie"):

        if not await self.sanction_possible(ctx, member): return

        await member.send(f"{member.mention} Vous avez été banni du serveur **{ctx.guild}** !")
        await member.ban(reason=reason)

        self.data.add_offense(ctx.guild.id, member.id, 3, 3, reason)

        embed = discord.Embed(title="Bannissement Effectué", description="Vous avez banni un membre", color=0x00FF4D)
        embed.add_field(name="Utilisateur", value=str(member), inline=False)
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="Aucune raison fournie"):
        await ctx.guild.unban(user=user, reason=reason)

        embed = discord.Embed(title="Débannissement Effectué", description="Vous avez débanni un membre", color=0x00FF4D)
        embed.add_field(name="Utilisateur", value=str(user), inline=False)
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, messages: int):
        if 1 <= messages <= 100:
            await ctx.channel.purge(limit=messages)
            embed = discord.Embed(title="Purge Effectuée", description="Vous avez purgé un salon", color=0x00FF4D)
            embed.add_field(name="Salon", value=ctx.channel.mention, inline=False)
            embed.add_field(name="Messages", value=f"{messages} messages")
        else:
            embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
            embed.add_field(name="Raison", value="Vous devez choisir un nombre entre 1 et 100 inclus.", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def cooldown(self, ctx, channel: discord.TextChannel, delay: int):
        if 0 <= delay <= 300:
            await channel.edit(slowmode_delay=delay)

            embed = discord.Embed(title="Cooldown Effectué", description="Vous avez modifié un cooldown", color=0x00FF4D)
            embed.add_field(name="Salon", value=channel.mention, inline=False)
            embed.add_field(name="Délai", value=f"{delay // 60}min {delay % 60}s ({delay}s)")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Action Impossible", description="L'action est impossible à effectuer", color=0xFF0020)
            embed.add_field(name="Raison", value="Vous devez choisir un nombre entre 0 et 300 inclus.", inline=False)
            await ctx.send(embed=embed)
