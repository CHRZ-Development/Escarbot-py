from discord.ext import commands
from discord import Member


class BanCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.ban.add_check(self.bot.check_permission)

    @commands.command(name="ban")
    async def ban(self,ctx,member: Member,how_much_days,why): return await member.ban(reason=why)
