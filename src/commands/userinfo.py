from discord import Colour,Embed,utils
from discord.ext import commands


class UserInfoCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    async def info_user_message(self,ctx,arg):
        user = utils.get(ctx.guild.members,id=int(arg))
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
            for n,slc in enumerate(self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['WhenHeAtBeenBanned']):
                date_banned.append(str(self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['WhenHeAtBeenBanned'][slc]))
                if n <= 1:
                    date_banned.append("-")
            info_message.add_field(name="❌ **|** Le dernier BAN",
                                   value="📅 Quand:" + " ".join(date_banned) + f"""\n🕵️ Par qui: `{self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['BanInfo']['WhoAtBanned']}`
                                                                                     ❔ Pourquoi: `{self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["Why"]}`
                                                                                     💥 Definitive: `{"Non" if self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False else "Oui"}`
                                                                                     📅 Combient de jours: `{self.bot.users_data[str(user.guild.id)][str(user.id)]["CriminalRecord"]["BanSystem"]["how_much_days"]}`""",inline=False)
        else:
            info_message.add_field(name="❌ **|** Nombre de BAN(s) (**Faite attention !**):",value=f"`{self.bot.users_data[str(user.guild.id)][str(user.id)]['CriminalRecord']['NumberOfBans']}`",inline=False)
        if user.activity is None:
            info_message.add_field(name=f"👀 **|** Activitée:",value=f"`Rien`")
        else:
            info_message.add_field(name=f"👀 **|** Activitée:",value=f"`{user.activity.name}`")
        if user.voice is None:
            info_message.add_field(name=f"➡ **|** Connecté sur:",value=f"`Rien`")
        else:
            info_message.add_field(name=f"➡ **|** Connecté sur:",value=f"<#{user.voice.channel.id}>")
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

    @commands.command(name="userinfo",aliases=["ui"])
    async def user_info_command(self,ctx,*args):
        if args[0] == "me":
            return await self.info_user_message(ctx,ctx.author.id)
        return await self.info_user_message(ctx,args[0])
