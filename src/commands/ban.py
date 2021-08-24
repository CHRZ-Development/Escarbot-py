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
        return await member.ban(reason=why)
