from discord.ext import commands
from discord import utils


class BanCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.ban.add_check(self.bot.check_permission)

    @commands.command(name="ban")
    async def ban(self,ctx,member_id,how_much_days,why):
        """ ban_command() -> !ban 842033926012403783 5 "Je ne sais pas"
            * It allow to ban a member ! """
        member = utils.get(ctx.guild.members,id=int(member_id))
        self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["IsBanned"] = True
        if self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Why"] is not None:
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Why"].append(why)
        else:
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Why"] = [why]
        if self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhoAtBanned"] is not None:
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhoAtBanned"].append(ctx.author.name)
        else:
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["WhoAtBanned"] = [ctx.author.name]
        if how_much_days == "def":
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanInfo"]["Definitive"] = True
        else:
            self.bot.users_data[str(ctx.guild.id)][member_id]["CriminalRecord"]["BanSystem"] = {"day_counter": 0,"how_much_days": how_much_days}
            if self.bot.users_data[str(ctx.guild.id)][str(ctx.id)]['CriminalRecord']['BanInfo']['TimeOfBan']["Day"] is not None:
                self.bot.users_data[str(ctx.guild.id)][str(ctx.id)]['CriminalRecord']['BanInfo']['TimeOfBan']["Day"].append(how_much_days)
            else:
                self.bot.users_data[str(ctx.guild.id)][str(ctx.id)]['CriminalRecord']['BanInfo']['TimeOfBan']["Day"] = [how_much_days]
        return await member.ban(reason=why)
