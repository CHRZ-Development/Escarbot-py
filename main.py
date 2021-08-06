# -*- coding: UTF-8 -*-
"""
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
===========================================================================
"""
import os
import json
import datetime

from discord.ext import commands
from discord import Intents,Embed,Status

from src.commands.help import HelpCommand
from src.commands.edit import EditCommand
from src.commands.messages import MessagesCommand
from src.commands.public import PublicVocalCommand
from src.commands.private import PrivateVocalCommand
from src.commands.attributes import AttributesCommand
from src.commands.rename import RenameVocalChannelCommand

from src.activities import Activities
from src.roles_sytem import RolesSystem
from src.analytics_system import Analytics
from src.backup_system import BackupSystem
from src.notif_system import NotificationSystem
from src.vocal_salon_system import VocalSalonSystem

from src.scripts import log_settings
from src.file_manager import FileManager


def set_permissions() -> Intents:
    """ set_permission() -> All permission for the Bot."""
    perms = Intents.all()
    perms.guilds = True
    perms.members = True
    perms.messages = True
    perms.reactions = True
    perms.presences = True
    perms.voice_states = True
    perms.guild_messages = True
    perms.guild_reactions = True
    return perms


file = FileManager()
config = file.load("cfg.ini",f"{os.getcwd()}/res/")
log_settings()


class Bot(commands.Bot):
    """ Bot() -> Represent a Bot discord """
    def __init__(self):
        commands.Bot.__init__(self,intents=set_permissions(),command_prefix="!",help_command=None)
        self.config = config
        self.file = file
        self.template = {"roles_can_attributes": [],"roles_emoji_reaction": {},"functions": {"stat": False,"verif_rules": True,"create_personal_vocal": False},"categories_ID": {"vocals_channel": 0},"vocals_ID": {"create_vocal": 0},"messages_ID": {"roles": 0,"rules": 0,"stat": 0,},"messages": {"welcome": [],"rules": {"authorized": [],"forbidden": [],"verif_rules": ["> Avez-vous pris connaisance des régles ?","Si oui, clické sur la reaction ci-dessous"]}},"roles": {},"roles_info": {}}

        guilds_data_path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
        with open(guilds_data_path) as f:
            self.guilds_data = json.load(f)

        self.create_embed = lambda title,description,color: Embed(title=title,description=description,color=color)
        self.add_all_cogs()

    def add_all_cogs(self):
        all_cogs = [BackupSystem(self),Analytics(self),EditCommand(self),MessagesCommand(self),AttributesCommand(self),RolesSystem(self),VocalSalonSystem(self),PrivateVocalCommand(self),PublicVocalCommand(self),RenameVocalChannelCommand(self),HelpCommand(self)]
        for cog in all_cogs:
            self.add_cog(cog)

    async def on_ready(self):
        await self.change_presence(activity=Activities(version=config["BOT"]["version"]),status=Status.do_not_disturb)
        print(f"[{datetime.datetime.today().date()}] I'm ready !")


escarbot = Bot()
escarbot.run(config["BOT"]["TOKEN"])

