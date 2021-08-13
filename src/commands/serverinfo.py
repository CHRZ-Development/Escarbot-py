from discord import Colour,Embed,Guild
from discord.ext import commands


class ServerInfoCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="serverinfo",aliases=["si"])
    async def server_info_command(self,ctx):
        guild: Guild = ctx.guild
        info_message = Embed(title=f"> **Information sur {guild.name}.**",colour=Colour.from_rgb(35,39,42))
        info_message.add_field(name="👮 Proprietaire:",value=f"_Name:_ `{guild.owner.name}`\n_ID:_ `{guild.owner.id}`")
        info_message.add_field(name="Serveur crée le:",value=f"`{guild.created_at}`")
