from discord.ext import commands
from discord import Colour,Embed,Member,utils
from discord.ext.commands import has_permissions


class AutoMessagesSendSystem(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    async def detect_role_changed(self,b,a):
        """ detect_role_changed( ) -> Notify hierarchical change
                :param b: before
                :param a: after """
        try:
            # Text Channel
            channel_lvlup = self.bot.get_channel(self.bot.guilds_data[str(b.guild.id)]["channels_ID"]["lvl_up"])
        except KeyError:
            return
        else:
            b_role,a_role = {},{}
            # If the roles at been changed
            if a.roles != b.roles:
                # Write all role between after and before role attribute
                number_keys_b_role,number_keys_a_role = 0,0
                for role in b.roles:
                    b_role[role.name] = role
                    number_keys_b_role += 1
                for role in a.roles:
                    a_role[role.name] = role
                    number_keys_a_role += 1
                # If after attribute role as been changed
                if number_keys_a_role > number_keys_b_role:
                    change_role = a_role
                    compare_role = b_role
                else:
                    # Stop this function
                    return False
                # Detect the new name of role
                role_update = None
                for role in change_role:
                    try:
                        compare_role[role]
                    except KeyError:
                        role_update = role
                # Send the hierarchical changed
                level_up_message = Embed(title="> __**Niveau superieurs !**__",colour=Colour.from_rgb(102,255,255))
                level_up_message.add_field(name="**Vous avez eu un niveau superieurs**",value=f"Vous avez maintenant le rôle `{role_update}`.")
                level_up_message.set_author(name=a.name,icon_url=a.avatar_url)
                get_role = utils.get(a.guild.roles,name=role_update)
                if get_role.id == int(self.bot.guilds_data[str(a.guild.id)]["roles"]["✅"]):
                    await self.welcome_message(a)
                return await channel_lvlup.send(embed=level_up_message)

    async def welcome_message(self,member):
        text_channel = self.bot.get_channel(int(self.bot.guilds_data[str(member.guild.id)]["channels_ID"]["welcome_channel"]))
        welcome_message = Embed(title="> **Nice, un nouveau !** 👋",colour=Colour.from_rgb(0,128,255))
        welcome_message.add_field(name="Je te souhaite la bienvenue !",value=f"{member.mention}\nPrend un ☕ café et vient dans <#839042197629304853>, dit nous coucou ! 😄")
        welcome_message.set_author(name=member.name,icon_url=member.avatar_url)
        await text_channel.send(embed=welcome_message)

    async def create_vocal_message(self,member):
        text_channel = self.bot.get_channel(int(self.bot.guilds_data[str(member.guild.id)]["channels_ID"]["command_channel"]))
        create_vocal_message = Embed(title="> **Vous venez de crée un salon vocal !**",colour=Colour.from_rgb(96,96,96))
        create_vocal_message.add_field(name=f"Vous avez droit désormais grâce à votre salon:",value="Commandes:\n:white_small_square: `!myvocal` _(alias `!mv`)_\n_Pour plus d'info sur les commandes, entrez `!help <commande>`_\n\n:white_small_square: Ecouté de la <#867173777485725706>\n_Pour plus d'info sur le Bot musique, entrez `.help`_")
        create_vocal_message.set_author(name=member.name,icon_url=member.avatar_url)
        create_vocal_message.set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url)
        await text_channel.send(embed=create_vocal_message)

    async def ban_message(self,guild,member,how_much_days,why):
        # if a channel is attributed
        ban_message = Embed(title="> Oh ! Un ban... 🤨",color=Colour.from_rgb(255,0,0))
        msg_days_info = f"pour **{how_much_days} jours**" if self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False else "**définitivement**"
        # Text channel message
        ban_message.add_field(name=f"L'utilisateur {member.name} à étais banni·e",value=f"Banni·e {msg_days_info} pour avoir `{why}`")
        ban_message.set_author(name=member.name,icon_url=member.avatar_url)
        ban_message.set_image(url="https://media.giphy.com/media/l2Sqh1SNVIaVKzWVy/giphy.gif")
        # MP Message
        mp_ban_message = Embed(title=f"> Vous etes banni·e du serveur {guild.name}",color=Colour.from_rgb(255,0,0))
        mp_ban_message.add_field(name="__Information du ban__:", value=f"Vous etes banni·e {msg_days_info} pour avoir `{why}`")
        mp_ban_message.set_author(name=guild.name,icon_url=guild.icon_url)
        mp_ban_message.set_footer(text=member.name,icon_url=member.avatar_url)
        # Ticket message
        mp_ticket_message = Embed(title="> **Vous trouvez ce ban injustifier ?**",colour=Colour.from_rgb(255,0,0))
        mp_ticket_message.add_field(name="Voici un Discord pour pouvoir êtres en relaxion avec un membre du staff",value="__https://discord.gg/Se2phANYrG__")
        mp_ticket_message.set_footer(text=f"Signé {guild.owner.name}.",icon_url=guild.owner.avatar_url)
        await member.send(embed=mp_ban_message)
        await member.send(embed=mp_ticket_message)
        try:
            text_channel = utils.get(guild.text_channels,id=self.bot.guilds_data[str(guild.id)]["channels_ID"]["criminal_report"])
        except KeyError:
            pass
        else:
            await text_channel.send(embed=ban_message)

    async def check_user_booster(self,b: Member,a: Member):
        if b.premium_since == a.premium_since:
            return False
        guild = utils.get(self.bot.guilds,id=a.guild_id)
        if a.premium_since is None:
            return await a.remove_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))
        channel_lvlup = self.bot.get_channel(self.bot.ids[a.guild.id]["id_channel_lvlup"])
        await a.add_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))
        await channel_lvlup.send(embed=self.bot.create_embed("> __**Wow !**__",f"_ _\n**Merci** {a.mention} **d'avoir boost le serveur !** ❤ ! Vous avez maintenant accès à des avantages !\n_ _",0xff80c0))

    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        how_much_days = self.bot.users_data[str(guild.id)][str(user.id)]["CriminalRecord"]["BanSystem"]["how_much_days"]
        why = self.bot.users_data[str(guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["Why"]
        await self.ban_message(guild,user,how_much_days,why)

    @commands.Cog.listener()
    @has_permissions(manage_roles=True)
    async def on_member_update(self,before,after):
        await self.detect_role_changed(before,after)
        await self.check_user_booster(before,after)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if before.channel is not None:
            if int(before.channel.id) == int(self.bot.guilds_data[str(member.guild.id)]["vocals_ID"]["create_vocal"]):
                await self.create_vocal_message(member)

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        return await ctx.send(embed=Embed(title="> ⚠ **Commande introuvable !**",description=error,color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))

