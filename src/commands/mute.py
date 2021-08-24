from discord import Member,utils
from discord.ext import commands
from discord.ext.commands import Context

from exceptions.NoRoleAttribute import NoRoleAttribute
from src.exceptions.RoleMuteNotAttribute import RoleMuteNotAttribute


class MuteCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.mute.add_check(self.bot.check_permission)

    @commands.command(name="mute")
    async def mute(self,ctx: Context,member_id,how_much,raison):
        member: Member = utils.get(ctx.guild.members,id=int(member_id))
        for n,role_database in enumerate(self.bot.guilds_data[str(ctx.guild.id)]["roles"]):
            if role_database["role_name"] == "mute":
                role = utils.get(ctx.guild.roles,id=int(role_database["role_id"]))
                break
            if int(n) == len(self.bot.guilds_data[str(ctx.guild.id)]["roles"])-1:
                raise RoleMuteNotAttribute
        try:
            return await member.add_roles(role,reason=raison)
        except UnboundLocalError:
            raise NoRoleAttribute
