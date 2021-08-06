import os

from typing import List
from discord.ext import commands
from discord import Colour,Embed,utils


class BanCommand(commands.Cog):

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

    async def ban_message(self,ctx,member,how_much_days,why):
        # if a channel is attributed
        try:
            text_channel = utils.get(ctx.guild.text_channels,id=self.bot.guilds_data[str(ctx.guild.id)]["channels_ID"]["criminal_report"])
        except KeyError:
            return
        ban_message = Embed(title="> Oh ! Un ban... 🤨",color=Colour.from_rgb(255,0,0))
        ban_message.add_field(name=f"l'utilisateur {member.name} à étais banni·e",value=f"Banni·e pour {how_much_days} jours pour avoir {why}")
        ban_message.set_author(name=member.name,icon_url=member.avatar_url)
        ban_message.set_image(url="https://media.giphy.com/media/l2Sqh1SNVIaVKzWVy/giphy.gif")
        await text_channel.send(embed=ban_message)

    @commands.command(name="ban")
    async def ban_command(self,ctx,member_id,how_much_days,why):
        """ ban_command() -> !ban 842033926012403783 5 "Je ne sais pas"
            * It allow to ban a member ! """
        perm_check = await self.perm_check(ctx,self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"]["ban"])
        if perm_check == "pass":
            member = utils.get(ctx.guild.members,id=int(member_id))
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhoAtBanned"] = str(ctx.author.name)
            if how_much_days == "def":
                self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Definitive"] = True
            else:
                self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanSystem"] = {"day_counter": 0,"how_much_days": how_much_days}
            await self.ban_message(ctx,member,how_much_days,why)
            return await member.ban(reason=why)

