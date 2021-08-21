from discord import Colour,Embed,utils
from discord.ext import commands
from discord.ext.commands import Context,UserNotFound
from discord_slash import SlashContext,cog_ext
from discord_slash.utils.manage_commands import create_option


class UserInfo(object):
    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
        self.error_msg = [["⚠ Utilisateur non trouvé !",lambda error: self.bot.translator.translate(src="en",dest="fr",text=error).text]]

    async def info_user_message(self,ctx,arg):
        user = utils.get(ctx.guild.members,id=int(arg))
        if user is None:
            raise UserNotFound(f"{arg}")
        info_message = Embed(title=f"> 📰 **|** **Information sur {user}.**",colour=Colour.from_rgb(35,39,42))
        info_message.add_field(name="🏷 **|** Pseudo:",value=f"Serveur: `{user.display_name}`\nRéel: `{user.name}`")
        info_message.add_field(name="💳 **|** ID:",value=f"`{user.id}`")
        status = f"{'🟢' if str(user.status) == 'online' else '🟡' if str(user.status) == 'idle' else '🔴' if str(user.status) == 'dnd' else '⚪'}"
        info_message.add_field(name=f"{status} **|** Status:",value=f"`{user.status}`")
        info_message.add_field(name="📅 **|** Date de création:",value=f"`{user.created_at}`")
        info_message.add_field(name="➡ **|** Rejoin le serveur le:",value=f"`{user.joined_at}`")
        info_message.add_field(name="🔺 **|** Top rôle:",value=f"`{user.top_role}`")
        if self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["NumberOfBans"] >= 1:
            info_message.add_field(name="❌ **|** Nombre de BAN(s) (**Faite attention !**):",value=f"`{self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['NumberOfBans']}`",inline=False)
            date_banned = []
            for index in self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"]:
                if self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"][index] is not None:
                    for n in range(len(self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"][index])):
                        slc = n%3
                        date_banned.append(str(self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"][index][n%3]))
                        if slc <= 1 and slc != 2:
                            date_banned.append("-")
                        if slc == 2:
                            date_banned.append("\n")
            ban_why_info = "\n".join(self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["Why"])
            date_timeofban = []
            for index in self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["TimeOfBan"]:
                if self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["TimeOfBan"][index] is not None:
                    for n in range(len(self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['TimeOfBan'][index])):
                        slc = n%3
                        date_timeofban.append(str(self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['TimeOfBan'][index][n%3]))
                        if slc <= 1 and slc != 2:
                            date_timeofban.append("-")
                        if slc == 2:
                            date_timeofban.append("\n")
            how_much_day_info = "\n".join(date_timeofban)
            who_ban_info = "\n".join(self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['WhoAtBanned'])
            info_message.add_field(name="❌ **|** Info BAN",value="📅 Quand: `" + " ".join(date_banned) + f"""` \n🕵️ Par qui: `{who_ban_info}`
                                                                                                                ❔ Pourquoi: `{ban_why_info}`
                                                                                                                💥 Definitive: `{"Non" if self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False else "Oui"}`
                                                                                                                📅 Combient de jours: `{how_much_day_info}`""",inline=False)
        else:
            info_message.add_field(name="❌ **|** Nombre de BAN(s) (**Faite attention !**):",value=f"`{self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['NumberOfBans']}`",inline=False)
        info_message.add_field(name=f"👀 **|** Activitée:",value=f"`Rien`") if user.activity is None else info_message.add_field(name=f"👀 **|** Activitée:",value=f"`{user.activity.name}`")
        info_message.add_field(name=f"➡ **|** Connecté sur:",value=f"`Rien`") if user.voice is None else info_message.add_field(name=f"➡ **|** Connecté sur:",value=f"<#{user.voice.channel.id}>")
        roles = []
        for n,role in enumerate(user.roles):
            if n >= 1:
                roles.append(f" `{role.name}` ")
                roles.append("_**|**_")
        all_messages = 0
        for slc in self.bot.users_data[str(user.guild.id)][str(user.id)]["NumberOfMessages"]:
            all_messages += int(self.bot.users_data[str(user.guild.id)][str(user.id)]["NumberOfMessages"][slc])
        info_message.add_field(name=f"💬 **|** Nombres de messages envoyée:",value=f"`{all_messages}`")
        info_message.add_field(name="🎖 Rôles:",value=" ".join(roles),inline=False)
        info_message.set_author(name=user.name,icon_url=user.avatar_url)
        info_message.set_footer(text=f"Effectué avec succès grâce à Escarbot, votre serviteur !",icon_url=self.bot.user.avatar_url)
        return await ctx.send(embed=info_message)


class UserInfoCommand(UserInfo,commands.Cog):

    def __init__(self,bot):
        UserInfo.__init__(self,self,bot)
        self.bot = bot

    @commands.command(name="userinfo",aliases=["ui"])
    async def userinfo_command(self,ctx: Context,_id: str): return await self.info_user_message(ctx,int(ctx.author.id)) if _id == "me" else await self.info_user_message(ctx,int(_id))

    @userinfo_command.error
    async def userinfo_error(self,ctx: Context,error): return await self.bot.send_message_after_invoke(ctx,[],self.error_msg,error=error)


class UserInfoSlash(UserInfo,commands.Cog):
    userinfo_option = [create_option(name="identifiant",description="Specifié l'ID de l'utilisateur",required=True,option_type=3)]

    def __init__(self,bot):
        UserInfo.__init__(self,self,bot)
        self.bot = bot

    @cog_ext.cog_slash(name="userinfo",description="Donne des informations supplémentaires sur un utilisateur grâce à son ID",options=userinfo_option)
    async def userinfo(self,ctx: SlashContext,identifiant: str): return await self.info_user_message(ctx,int(ctx.author.id)) if identifiant == "me" else await self.info_user_message(ctx,int(identifiant))

    @userinfo.error
    async def userinfo_error(self,ctx: SlashContext,error): return await self.bot.send_message_after_invoke(ctx,[],self.error_msg,error=error)
