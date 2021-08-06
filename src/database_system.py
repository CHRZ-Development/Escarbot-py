import os
import datetime

from discord.ext import commands
from discord.ext.tasks import loop


class DataBaseSystem(commands.Cog):
    """ DataBaseSystem() -> Represent the DataBase management. """
    def __init__(self,bot):
        self.bot = bot

    def refresh_database(self):
        return self.bot.file.write(self.bot.guilds_data,"guilds_data.json",f"{os.getcwd()}/res/")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        self.bot.guilds_data[str(guild.id)] = self.bot.template
        self.refresh_database()

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        self.bot.guilds_data.pop(str(guild.id))
        self.refresh_database()

    @commands.Cog.listener()
    async def on_member_join(self,member):
        self.bot.guilds_data[str(member.guild.id)][str(member.id)] = self.bot.template_user
        self.refresh_database()

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        self.bot.guilds_data[str(member.guild.id)].pop(str(member.id))
        self.refresh_database()

    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        guild_id = str(guild.id)
        member_id = str(user.id)
        self.bot.users_data[guild_id][member_id]["CriminalRecord"]["BanInfo"]["IsBanned"] = True
        self.bot.users_data[guild_id][member_id]["CriminalRecord"]["NumberOfBans"] += 1
        year,month,day = str(datetime.datetime.today().date()).split('-')
        today_date_list = [year,month,day,0]
        for n,key in enumerate(self.bot.users_data[guild_id][member_id]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"]):
            self.bot.users_data[guild_id][member_id]["CriminalRecord"]["BanInfo"]["WhenHeAtBeenBanned"][key] = today_date_list[n]

    @commands.Cog.listener()
    async def on_member_unban(self,guild,user):
        self.bot.users_data[str(guild.id)][str(user.id)]["CriminalRecord"]["BanInfo"]["IsBanned"] = False
        self.refresh_database()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_unban.start()

    @loop(hours=24)
    async def check_unban(self):
        for guild in self.bot.guilds:
            # Check for each member
            for member in guild.members:
                if (self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["IsBanned"]) and (self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False):
                    if self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["day_counter"] >= self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["how_much_days"]:
                        self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanSystem"]["day_counter"] += 1
                    else:
                        await guild.unban(member)
        self.refresh_database()
