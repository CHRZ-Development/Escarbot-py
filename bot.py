# -*- coding: UTF-8 -*-
""" =======================================================================

     ██████   █████                      ████            ██████   █████
    ░░██████ ░░███                      ░░███           ░░██████ ░░███
     ░███░███ ░███   ██████   █████ ████ ░███   ██████   ░███░███ ░███
     ░███░░███░███  ░░░░░███ ░░███ ░███  ░███  ░░░░░███  ░███░░███░███
     ░███ ░░██████   ███████  ░███ ░███  ░███   ███████  ░███ ░░██████
     ░███  ░░█████  ███░░███  ░███ ░███  ░███  ███░░███  ░███  ░░█████
     █████  ░░█████░░████████ ░░████████ █████░░████████ █████  ░░█████
    ░░░░░    ░░░░░  ░░░░░░░░   ░░░░░░░░ ░░░░░  ░░░░░░░░ ░░░░░    ░░░░░

===========================================================================
◻ Doc discord.py: https://discordpy.readthedocs.io/en/stable/api.html
◻ Dev Discord Guild: https://discord.gg/yEvBg8CPaM
◻ YouTube Channel: https://www.youtube.com/channel/UCbl4AHVket_DNhBzQG56f7w
======================================================================= """
import os
import json
import datetime

from discord import Embed,Intents,Message
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import SlashCommand,SlashContext
from googletrans import Translator

from src.commands.ban import BanCommand
from src.commands.help import HelpCommand
from src.commands.edit import EditCommand
from src.commands.ping import PingCommand
from src.commands.unban import UnBanCommand
from src.commands.nickname import (NicknameCommand,NicknameSlash)
from src.commands.myvocal import (MyVocalCommand,MyVocalSlash)
from src.commands.userinfo import UserInfoCommand
from src.commands.messages import MessagesCommand
from src.commands.serverinfo import ServerInfoCommand
from src.commands.attributes import AttributesCommand
from src.activities import Activities
from src.roles_sytem import RolesSystem
from src.file_manager import FileManager
from src.analytics_system import Analytics
from src.backup_system import BackupSystem
from src.database_system import DataBaseSystem
from src.notif_system import NotificationSystem
from src.vocal_salon_system import VocalSalonSystem
from src.auto_messages_send_system import AutoMessagesSendSystem


def set_permissions() -> Intents:
    """ set_permission() -> All permission for the Bot."""
    perms = Intents.all()
    perms.bans = True
    perms.guilds = True
    perms.members = True
    perms.messages = True
    perms.reactions = True
    perms.presences = True
    perms.voice_states = True
    perms.guild_messages = True
    perms.guild_reactions = True
    return perms


class Bot(commands.Bot):
    """ Bot() -> Represent a Bot discord """
    def __init__(self):
        commands.Bot.__init__(self,intents=set_permissions(),command_prefix="!",help_command=None)
        self.slash = SlashCommand(client=self,sync_commands=True,override_type=True)
        self.file = FileManager()
        self.translator = Translator()
        self.config = self.file.load("cfg.ini",f"{os.getcwd()}/res/")
        # Messages
        self.titles = ["> ❌ | Erreur !","> ✅ | Effectué !"]
        self.success_footer = ["Effectué avec succès grâce à Escarbot, votre serviteur !","Utilisé les nouvelles commandes slash ! Effectué avec succès grâce à Escarbot, votre serviteur !"]
        self.error_footer = ["Escarbot n'a pas pu effectué votre demande !","Utilisé les nouvelles commandes slash ! Escarbot n'a pas pu effectué votre demande !"]
        # Template for database
        self.template = {"roles_can_attributes": [],"roles_emoji_reaction": {},"functions": {"stat": False,"verif_rules": True,"create_personal_vocal": False},"categories_ID": {"vocals_channel": 0},"vocals_ID": {"create_vocal": 0},"messages_ID": {"roles": 0,"rules": 0,"stat": 0,},"messages": {"welcome": [],"rules": {"authorized": [],"forbidden": [],"verif_rules": ["> Avez-vous pris connaisance des régles ?","Si oui, clické sur la reaction ci-dessous"]}},"roles": {},"roles_info": {}}
        self.template_user = {"JoinedAt": {"Year": 0,"Month": 0,"Day": 0},"CriminalRecord": {"NumberOfWarnings": 0,"NumberOfReports": 0,"NumberOfBans": 0,"BanInfo": {"Definitive": False,"IsBanned": False,"WhoAtBanned": None,"WhenHeAtBeenBanned": {"Year": None,"Month": None,"Day": None,"Hour": None},"TimeOfBan": {"Year": None,"Month": None,"Day": None,"Hour": None}},"BanSystem": {"day_counter": 0,"how_much_days": 0},"ReportInfo": {"NumberOfReports": 0,"WhoReportedIt": {"Users": [],"When": [],"Messages": []}},"RestrictedInfo": {"IsRestricted": False,"WhoAtRestricted": None,"WhenHeAtBeenRestricted": {"Year": None,"Month": None,"Day": None,"Hour": None},"TimeOfRestricted": {"Year": None,"Month": None,"Day": None}}},"NumberOfMessages": {"2021-06": 169,"2021-07": 48}}
        # Guilds settings
        guilds_data_path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
        with open(guilds_data_path) as f:
            self.guilds_data = json.load(f)
        # User database per guilds
        user_info_path = os.path.join(f"{os.getcwd()}/res/","users_data.json")
        with open(user_info_path) as f:
            self.users_data = json.load(f)
        # Add all commands and systems
        self.add_all_cogs()

    async def send_message_after_invoke(self,ctx,success_msg,error_msg,action=None,value=None,error=None):
        msg = Embed(title=self.titles[0] if value is None else self.titles[1])
        # Send successfully message embed
        if value is not None:
            msg.add_field(name=success_msg[0],value=success_msg[1](value))
            if isinstance(ctx,SlashContext) or isinstance(ctx,Message):
                msg.set_footer(text=self.success_footer[0],icon_url=self.user.avatar_url)
            if isinstance(ctx,Context):
                msg.set_footer(text=self.success_footer[1],icon_url=self.user.avatar_url)
        # Send error message embed
        if error is not None:
            msg.add_field(name=error_msg[0][0],value=error_msg[0][1](error))
            try:
                msg.add_field(name=error_msg[1][0],value=error_msg[1][1],inline=False)
            except KeyError:
                pass
            if isinstance(ctx,SlashContext) or isinstance(ctx,Message):
                msg.set_footer(text=self.error_footer[0],icon_url=self.user.avatar_url)
            if isinstance(ctx,Context):
                msg.set_footer(text=self.error_footer[1],icon_url=self.user.avatar_url)
        msg.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        if isinstance(ctx,Message):
            return await ctx.channel.send(embed=msg)
        if isinstance(ctx,SlashContext):
            return await ctx.send(embed=msg,components=action)
        return await ctx.send(embed=msg)

    def add_all_cogs(self):
        all_slashes = [NicknameSlash(self),MyVocalSlash(self)]
        for slash in all_slashes:
            self.slash.get_cog_commands(slash)
        self.add_cog(all_slashes[0])
        all_commands = [NicknameCommand(self),ServerInfoCommand(self),UserInfoCommand(self),PingCommand(self),MyVocalCommand(self),UnBanCommand(self),BanCommand(self),EditCommand(self),MessagesCommand(self),AttributesCommand(self),HelpCommand(self)]
        for command in all_commands:
            self.add_cog(command)
        all_systems = [NotificationSystem(self),DataBaseSystem(self),AutoMessagesSendSystem(self),BackupSystem(self),Analytics(self),RolesSystem(self),VocalSalonSystem(self)]
        for system in all_systems:
            self.add_cog(system)

    async def on_ready(self):
        await self.change_presence(activity=Activities(version=self.config["BOT"]["version"]))
        print(f"==================================================")
        print(f"✅ Est lancée depuis {datetime.datetime.today().date()}")
        print(f"🤖 Bot: {self.user.name}")
        print(f"🟢 Connecté sur: {len(self.guilds)} serveurs")
        print(f"==================================================")
        print(f"[{datetime.datetime.today().date()}] Je suis prêt ! 👌")
