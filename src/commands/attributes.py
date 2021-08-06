# -*- coding: UTF-8 -*-
import os

from typing import List
from discord.ext import commands
from discord import Colour,Embed,utils


class AttributesCommand(commands.Cog):
    """ AttributesCommand() -> Represent the Server Configurator """
    def __init__(self,bot):
        self.bot = bot
        self.attribute_func = {"role_emoji": self.attribute_role_emoji,"role_info": self.attribute_role_info,"role": self.attribute_role,"members_stat": self.attribute_stat_members_channel,"rules_message": self.attribute_rules_message,"create_personal_vocal": self.attribute_create_vocal_channel,"perm_command": self.attribute_perm_commands,"criminal_report_channel": self.attribute_criminal_report_channel,"video_notif_channel": self.attribute_video_notif_channel,"live_notif_channel": self.attribute_live_notif_channel,"lvl_up_channel": self.attribute_level_up_channel}
        self.refresh_database = lambda: self.bot.file.write(self.bot.guilds_data,"guilds_data.json",f"{os.getcwd()}/res/")

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

    async def attribute_role_emoji(self,ctx,args):
        """ attribute_role_emoji() -> !attribute role_emoji *args
            * It allow to attribute an emoji has each role !
                :param args: role emoji | ex: member_role 👤 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            role,emoji = args
            guild_id = str(ctx.guild.id)
            self.bot.guilds_data[guild_id]["roles_emoji_reaction"][role] = emoji
            # None info for the new role by default.
            self.bot.guilds_data[guild_id]["roles_info"][role] = None
            # If not have doubloon.
            if self.bot.guilds_data[guild_id]["roles_can_attributes"].count(role) == 0:
                self.bot.guilds_data[guild_id]["roles_can_attributes"].append(role)
            self.refresh_database()

    async def attribute_role_info(self,ctx,args):
        """ attribute_role_emoji() -> !attribute role_info *args
            * It allow to attribute an info has each role ! (For role attribute message)
                :param args: role info | ex: member_role "Default role" """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            role,info = args
            self.bot.guilds_data[str(ctx.guild.id)]["roles_info"][role] = info
            self.refresh_database()

    async def attribute_role(self,ctx,args):
        """ attribute_role() -> !attribute role *args
            * It allow to attribute the role at an emoji ! (For role attribute message)
                :param args: emoji role_id | ex: 👤 852576991504105514 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            emoji,role_id = args
            self.bot.guilds_data[str(ctx.guild.id)]["roles"][emoji] = int(role_id)
            self.refresh_database()

    async def attribute_stat_members_channel(self,ctx,args):
        """ attribute_stat_members_channel() -> !attribute members_stat *args
            * It allow to display the members total stat in a guild !
                :param args: vocal_id | ex: 852576991504105514 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            # Enable the functionality
            self.bot.guilds_data[guild_id]["functions"]["stat"] = True
            self.bot.guilds_data[guild_id]["messages_ID"]["stat"] = int(args[0])
            self.refresh_database()

    async def attribute_rules_message(self,ctx,args):
        """ attribute_rules_message() -> !attribute rules_message *args
            * It allow to enable a little verification on the server when he/she join this one !
                :param args: message_id | ex: 852576991504105514 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            self.bot.guilds_data[guild_id]["messages_ID"]["rules"] = int(args[0])
            self.refresh_database()

    async def attribute_criminal_report_channel(self,ctx,args):
        """ attribute_criminal_report_channel() -> !attribute criminal_report_channel *args
            * It allow to display who as been banned !
                :param args: channel_id | ex: 852576991504105514 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            try:
                self.bot.guilds_data[guild_id]["channels_ID"]
            except KeyError:
                self.bot.guilds_data[guild_id]["channels_ID"] = {}
                self.bot.guilds_data[guild_id]["channels_ID"]["criminal_report"] = int(args[0])
            else:
                self.bot.guilds_data[guild_id]["channels_ID"]["criminal_report"] = int(args[0])
            self.refresh_database()

    async def attribute_video_notif_channel(self,ctx,args):
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            try:
                self.bot.guilds_data[guild_id]["channels_ID"]
            except KeyError:
                self.bot.guilds_data[guild_id]["channels_ID"] = {}
                self.bot.guilds_data[guild_id]["channels_ID"]["video_notif"] = int(args[0])
            else:
                self.bot.guilds_data[guild_id]["channels_ID"]["video_notif"] = int(args[0])
            self.refresh_database()

    async def attribute_level_up_channel(self,ctx,args):
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            try:
                self.bot.guilds_data[guild_id]["channels_ID"]
            except KeyError:
                self.bot.guilds_data[guild_id]["channels_ID"] = {}
                self.bot.guilds_data[guild_id]["channels_ID"]["lvl_up"] = int(args[0])
            else:
                self.bot.guilds_data[guild_id]["channels_ID"]["lvl_up"] = int(args[0])
            self.refresh_database()


    async def attribute_live_notif_channel(self,ctx,args):
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            try:
                self.bot.guilds_data[guild_id]["channels_ID"]
            except KeyError:
                self.bot.guilds_data[guild_id]["channels_ID"] = {}
                self.bot.guilds_data[guild_id]["channels_ID"]["live_notif"] = int(args[0])
            else:
                self.bot.guilds_data[guild_id]["channels_ID"]["live_notif"] = int(args[0])
            self.refresh_database()

    async def attribute_create_vocal_channel(self,ctx,args):
        """ attribute_create_vocal_channel() -> !attribute create_vocal_channel *args
            * It allow to can create a channel custom with anyone !
                :param args: vocal_id | ex: 852576991504105514 """
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            guild_id = str(ctx.guild.id)
            vocal_id = args[0]
            vocal_channel = utils.get(ctx.guild.voice_channels,id=int(vocal_id))
            # Enable the functionality
            self.bot.guilds_data[guild_id]["functions"]["create_personal_vocal"] = True
            self.bot.guilds_data[guild_id]["vocals_ID"]["create_vocal"] = int(vocal_id)
            self.bot.guilds_data[guild_id]["categories_ID"]["vocals_channel"] = int(vocal_channel.category_id)
            self.refresh_database()

    async def attribute_perm_commands(self,ctx,args):
        perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles) - 1].id])
        if perm_check == "pass":
            command,role = args
            try:
                self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"][command]
            except KeyError:
                self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"][command] = []
                self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"][command].append(int(role))
            else:
                self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"][command].append(int(role))
            self.refresh_database()

    @commands.command(name="attribute")
    @commands.is_owner()
    async def attribute_value(self,ctx,option,*args):
        """ attribute_value() -> !attribute
            * It allow to settings the server (Only owner can execute this command) """
        try:
            await self.attribute_func[option](ctx,args)
        except KeyError:
            return await ctx.send(embed=Embed(title="> **⚠ Attention !**",description="Cette commande n'existe ou verifié l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
        await ctx.message.delete()

