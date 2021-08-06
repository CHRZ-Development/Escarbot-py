import os

from typing import List
from discord import Colour,Embed
from discord.ext import commands


class UnBanCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.user_info_path = os.path.join(f"{os.getcwd()}/res/","user_data.json")

    @staticmethod
    async def perm_check(ctx,roles_list: List[int]):
        """ perm_check() -> Check if the user who as executed a command have authorization. """
        for n,role in enumerate(ctx.author.roles):
            # If authorized
            if role.id in roles_list:
                return "pass"
            # Not authorized
            if n == len(ctx.author.roles) - 1:
                return await ctx.send(embed=Embed(title="> **⚠ Attention !**",description="Vous n'avez pas la permission d'éxecutez cette commande !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))

    @commands.command(name="unban")
    async def unban_command(self,ctx,member_id):
        """ unban_command() -> !unban user_id """
        perms_check = await self.perm_check(ctx,self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"]["ban"])
        if perms_check == "pass":
            for n,member in enumerate(await ctx.guild.bans()):
                if member.user.id == int(member_id):
                    await ctx.guild.unban(member.user)
                if n == len(await ctx.guild.ban())-1:
                    return await ctx.send(embed=Embed(title="UUuuuh ?",description=f"Impossible d'enlevé le ban de {member_id} car l'utilisateur est inconnu !",colour=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))

