from discord import Colour,Embed,Guild
from discord.ext import commands
from discord_slash import cog_ext


async def server_info_message(self,ctx):
    guild: Guild = ctx.guild
    info_message = Embed(title=f"> 📰 **|** **Information sur {guild.name}.**",description=f"{guild.description}",colour=Colour.from_rgb(35,39,42))
    total_members = 0
    all_status_members = {"online": 0,"dnd": 0,"offline": 0,"idle": 0}
    for n,member in enumerate(guild.members):
        if member.bot is False:
            all_status_members[str(member.status)] += 1
            total_members += 1
    status_emojies = ["🟢","🔴","⚪","🟡"]
    for n,status in enumerate(all_status_members):
        info_message.add_field(name=f"{status_emojies[n]} **|** Status",value=f"`{all_status_members[status]}`")
        if n == 0:
            info_message.add_field(name="👮 **|** Proprietaire:",value=f"<@{guild.owner.id}>")
            info_message.add_field(name="📅 **|** Crée:",value=f"`{guild.created_at.date()}`")
        if n == 1:
            info_message.add_field(name="👤 **|** Membres:",value=f"`{total_members}`")
            info_message.add_field(name="💎 **|** Nitro Boost",value=f"`{guild.premium_tier}`")
        if n == 2:
            aliases_region = []
            for n,letter in enumerate(str(guild.region)):
                aliases_region.append(letter)
                if n == 1:
                    break
            info_message.add_field(name="🌍 **|** Région:",value=f":flag_" + "".join(aliases_region) + f": `{guild.region}`")
            info_message.add_field(name="☕ **|** Salons:",value=f"`{len(guild.channels)}`")
        if n == 3:
            info_message.add_field(name="🏅 **|** Rôles:",value=f"`{len(guild.roles)}`")
            info_message.add_field(name="💳 **|** ID:",value=f"`{guild.id}`")
    info_message.set_author(name=guild.name,icon_url=guild.icon_url)
    info_message.set_footer(text=f"Effectué avec succès grâce à Escarbot, votre serviteur !",icon_url=self.bot.user.avatar_url)
    return await ctx.send(embed=info_message)


class ServerInfoCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="serverinfo",aliases=["si"])
    async def server_info_command(self,ctx): return await server_info_message(self,ctx)


class ServerInfoSlash(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @cog_ext.cog_slash(name="serverinfo",description="Vous renvoie un message qui contient les infos supplémentaires du serveur !")
    async def serverinfo(self,ctx): return await server_info_message(self,ctx)
