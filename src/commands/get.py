from discord import Embed
from discord.ext import commands

from src.exceptions.InvalidSubcommand import InvalidSubcommand


class GetCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.subcommand = {"roles": self.get_role_attributed}

    async def info_role_msg(self,ctx,n,role_database):
        role_name = f"rôle name = '{role_database['role_name'] if role_database['role_name'] != '' else 'NameError'}'"
        role_id = f"rôle id = {role_database['role_id']}"
        role_emoji = f"rôle emoji = '{role_database['emoji']}'"
        role_info = f"rôle info = '{role_database['info']}'"
        role_command_perm = f"rôle command perm = {role_database['can_execute_command']}"
        msg = Embed(title=f"Page n°{n}").add_field(name=f"Données pour {role_database['role_name'] if role_database['role_name'] != '' else 'NameError'}",value="```python\n"+"\n".join([role_name,role_id,role_info,role_emoji,role_command_perm])+"```")
        return await ctx.send(embed=msg)

    async def get_role_attributed(self,ctx,args):
        for n,role_database in enumerate(self.bot.guilds_data[str(ctx.guild.id)]["roles"]):
            if len(args) == 0:
                await self.info_role_msg(ctx,n,role_database)
            if len(args):
                roles = str(args[0]).split(",")
                if len(roles) >= 2:
                    for role_id in roles:
                        if int(role_database["role_id"]) == int(role_id):
                            await self.info_role_msg(ctx,n,role_database)
                else:
                    if int(role_database["role_id"]) == int(args[0]):
                        await self.info_role_msg(ctx,n,role_database)

    @commands.command(name="get")
    @commands.is_owner()
    async def get_command(self,ctx,option,*args):
        try:
            await self.subcommand[option](ctx,args)
        except KeyError:
            raise InvalidSubcommand(option)
        await ctx.message.delete()
