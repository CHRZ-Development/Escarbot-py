import os
import json
import datetime

from typing import List
from discord.ext import commands
from discord.ext.tasks import loop
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

            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["IsBanned"] = True
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["NumberOfBans"] += 1

            year,month,day = str(datetime.datetime.today().date()).split('-')
            today_date_list = [year,month,day,0]
            for n,key in enumerate(self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"]):
                self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"][key] = today_date_list[n]

            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhoAtBanned"] = str(ctx.author.name)
            if how_much_days == "def":
                self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Definitive"] = True
            else:
                self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanSystem"] = {"day_counter": 0,"how_much_days": how_much_days}

            # Refresh database
            with open(self.user_info_path,"w") as f:
                json.dump(self.bot.users_data,f)

            await self.ban_message(ctx,member,how_much_days,why)
            return await member.ban(reason=why)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_unban.start()

    @loop(hours=24)
    async def check_unban(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if (self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["IsBanned"]) and (self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False):
                    if self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["day_counter"] >= self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["how_much_days"]:
                        self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["day_counter"] += 1
                    else:
                        await member.unban()

        with open(self.user_info_path,"w") as f:
            json.dump(self.bot.users_data,f)
