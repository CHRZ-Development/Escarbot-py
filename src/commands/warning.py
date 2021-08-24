from discord.ext import commands


class WarningCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="warning",aliases=["warn"])
    async def warning(self,ctx,member_id,how_much,reason):
        pass
