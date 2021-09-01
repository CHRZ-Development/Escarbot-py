# -*- coding: UTF-8 -*-
import os

from discord.ext import commands
from discord import utils

from src.exceptions.AlreadyAttribute import AlreadyAttribute
from src.exceptions.ArgumentError import ArgumentError
from src.exceptions.InvalidSubcommand import InvalidSubcommand


class AttributesCommand(commands.Cog):
    """ AttributesCommand() -> Represent the Server Configurator """
    def __init__(self,bot):
        self.bot = bot
        self.attribute_func = {"can_attribute_role": self.role_can_attribute,"role": self.attribute_role,"channel": self.attribute_channel}
        self.refresh_database = lambda: self.bot.file.write(self.bot.guilds_data,"guilds_data.json",f"{os.getcwd()}/res/")
        self.attribute.add_check(self.bot.check_permission)

    async def role_can_attribute(self,ctx,args):
        """ attribute_role_emoji() -> !attribute role_emoji *args
            * It allow to attribute an emoji has each role !
                :param args: page role | ex: 1 852576991504105514 """
        try:
            page,roles_id = args
        except ValueError:
            raise ArgumentError(args)
        else:
            if len(args) > 2:
                raise ArgumentError(args)
            guild_id = str(ctx.guild.id)
            try:
                self.bot.guilds_data[guild_id]["roles_can_attributes"][str(page)]
            except KeyError:
                self.bot.guilds_data[guild_id]["roles_can_attributes"][str(page)] = []
            # If not have doubloon.
            for role_id in str(roles_id).split(","):
                if self.bot.guilds_data[guild_id]["roles_can_attributes"][str(page)].count(int(role_id)) == 0:
                    self.bot.guilds_data[guild_id]["roles_can_attributes"][str(page)].append(int(role_id))
                    self.refresh_database()
                else:
                    raise AlreadyAttribute(roles_id)

    async def attribute_channel(self,ctx,args):
        try:
            channel_id,function,info = args
        except ValueError:
            raise ArgumentError(args)
        else:
            if len(args) > 3:
                raise ArgumentError(args)
            channel = await self.bot.fetch_channel(int(channel_id))
            self.bot.guilds_data[str(ctx.guild.id)]["channels"].append({"function": str(function).split(","),"channel_id": channel_id,"info": info,"channel_name": channel.name, "category_id": channel.category_id})
            self.refresh_database()

    async def attribute_role(self,ctx,args):
        """ attribute_role() -> !attribute role *args
            * It allow to attribute the role at an emoji ! (For role attribute message)
                :param args: role_id emoji info | ex: 852576991504105514 👤 "Default rôle" "" """
        try:
            role_id,emoji,info,can_execute_command = args
        except KeyError:
            raise ArgumentError(args)
        else:
            if len(args) > 4:
                raise ArgumentError(args)
            role = utils.get(ctx.guild.roles,id=int(role_id))
            self.bot.guilds_data[str(ctx.guild.id)]["roles"].append({"role_name": role.name,"role_id": role_id,"emoji": emoji,"info": info,"can_execute_command": str(can_execute_command).split(",")})
            self.refresh_database()

    @commands.command(name="attribute")
    async def attribute(self,ctx,option,*args):
        """ attribute_value() -> !attribute
            * It allow to settings the server (Only owner can execute this command) """
        try:
            await self.attribute_func[option](ctx,args)
        except KeyError:
            raise InvalidSubcommand(option)
        return await ctx.message.delete()
