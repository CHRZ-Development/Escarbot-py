from discord import Embed
from discord.ext import commands

from src.exceptions.InvalidSubcommand import InvalidSubcommand


class GetCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.subcommand = {"icon_server": self.get_avatar_server,"my_avatar": self.get_avatar_user,"roles": self.get_role_attributed,"channels": self.get_channel_attribute}
        self.infos = {"roles": self.info_role_msg,"channels": self.info_channel_msg}
        self.get.add_check(self.bot.check_permission)

    async def info_role_msg(self,ctx,n,role_database):
        role_name = f"rôle_name = '{role_database['role_name'] if role_database['role_name'] != '' else 'NameError'}'"
        role_id = f"rôle_id = {role_database['role_id']}"
        role_emoji = f"rôle_emoji = '{role_database['emoji']}'"
        role_info = f"rôle_info = '{role_database['info']}'"
        role_command_perm = f"rôle_command_perm = {role_database['can_execute_command']}"
        msg = Embed(title=f"Page_n°{n}").add_field(name=f"Données pour {role_database['role_name'] if role_database['role_name'] != '' else 'NameError'}",value="```python\n"+"\n".join([role_name,role_id,role_info,role_emoji,role_command_perm])+"```")
        return await ctx.send(embed=msg)

    async def info_channel_msg(self,ctx,n,channel_database):
        channel_name = f"channel_name = '{channel_database['channel_name']}'"
        channel_id = f"channel_id = {channel_database['channel_id']}"
        category_id = f"category_id = {channel_database['category_id']}"
        channel_function = f"function = {channel_database['function']}"
        channel_info = f"info = '{channel_database['info']}'"
        msg = Embed(title=f"Page_n°{n}").add_field(name=f"Données pour {channel_name}",value="```python\n"+"\n".join([channel_name,channel_id,category_id,channel_function,channel_info])+"```")
        return await ctx.send(embed=msg)

    async def get_system(self,ctx,args,what):
        for n,database in enumerate(self.bot.guilds_data[str(ctx.guild.id)][what[0]]):
            if len(args) == 0:
                await self.infos[what[0]](ctx,n,database)
            if len(args):
                roles = str(args[0]).split(",")
                if len(roles) >= 2:
                    for role_id in roles:
                        if int(database[what[1]]) == int(role_id):
                            await self.infos[what[0]](ctx,n,database)
                else:
                    if int(database[what[1]]) == int(args[0]):
                        await self.infos[what[0]](ctx,n,database)

    async def get_role_attributed(self,ctx,args): await self.get_system(ctx,args,("roles","role_id"))

    async def get_channel_attribute(self,ctx,args): await self.get_system(ctx,args,("channels","channel_id"))

    async def get_avatar_server(self,ctx,args): return await ctx.send(embed=Embed().set_image(url=ctx.guild.icon_url).set_author(name=ctx.guild.name,url=ctx.guild.icon_url))

    async def get_avatar_user(self,ctx,args): return await ctx.send(embed=Embed().set_image(url=ctx.author.avatar_url).set_author(name=ctx.author.name,url=ctx.author.avatar_url))

    @commands.command(name="get")
    async def get(self,ctx,option,*args):
        try:
            await self.subcommand[option](ctx,args)
        except KeyError:
            raise InvalidSubcommand(option)
        await ctx.message.delete()
