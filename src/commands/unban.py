from discord import Colour,Embed
from discord.ext import commands


class UnBanCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.unban.add_check(self.bot.check_permission)

    @commands.command(name="unban")
    async def unban(self,ctx,member_id):
        """ unban_command() -> !unban user_id """
        for n,member in enumerate(await ctx.guild.bans()):
            if member.user.id == int(member_id):
                return await ctx.guild.unban(member.user)
            if n == len(await ctx.guild.ban())-1:
                return await ctx.send(embed=Embed(description=f"`❌` | Impossible d'enlever le ban de `{member_id}` car l'utilisateur est inconnu·e !",colour=Colour.from_rgb(0,185,0)).set_author(name=f"Executée par {ctx.author.name}",icon_url=ctx.author.avatar_url))
        return await ctx.send(embed=Embed(colour=Colour.from_rgb(0,0,0)).add_field(name="Mais... 🤨",value=f"Impossible d'enlevé le ban de `{member_id}` car personne n'a étais banni·e sur `{ctx.guild.name}` !").set_author(name=f"Executée par {ctx.author.name}",icon_url=ctx.author.avatar_url))
