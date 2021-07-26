# -*- coding: UTF-8 -*-
# https://discord.gg/yEvBg8CPaM
# https://www.youtube.com/channel/UCbl4AHVket_DNhBzQG56f7w
import os

from discord import Intents,Embed
from discord.ext import commands

from commands.private import PrivateVocalCommand
from commands.public import PublicVocalCommand
from commands.rename import RenameVocalChannelCommand
from vocal_salon_system import VocalSalonSystem
from activities import Activities
from analytics_system import Analytics
from backup_system import BackupSystem
from commands.edit import EditCommand
from commands.send import SendCommand
from database_refresh import DataBase
from notif_system import NotificationSystem
from roles_sytem import RolesSystem
from file_manager import FileManager


def set_permissions():
	perms = Intents.all()
	perms.presences = True
	perms.members = True
	perms.messages = True
	perms.guilds = True
	perms.guild_messages = True
	perms.guild_reactions = True
	perms.reactions = True
	perms.voice_states = True
	return perms


file = FileManager()
config = file.load('cfg.ini',f'{os.getcwd()}/res/')


class Bot(commands.Bot):

	def __init__(self):
		commands.Bot.__init__(self,command_prefix='!',intents=set_permissions())

		# ID Guilds
		self.chrz_development = 838862631284506705
		self.aventurabuild = 846458770963169360
		self.emoji_check = "✅"
		self.actv = Activities(version=config["BOT"]["version"])

		self.file = file
		guilds_data = self.file.load('guilds_data.json', f'{os.getcwd()}/res/')
		self.roles_index = {838862631284506705: guilds_data["838862631284506705"]["roles_index"],
							846458770963169360: guilds_data["846458770963169360"]["roles_index"]}
		self.attribute_index = {838862631284506705: guilds_data["838862631284506705"]["attribute_index"],
								846458770963169360: guilds_data["846458770963169360"]["attribute_index"]}
		self.ids = {838862631284506705: guilds_data["838862631284506705"]["ids"],
					846458770963169360: guilds_data["846458770963169360"]["ids"]}

		self.create_embed = lambda title,description,color: Embed(title=title,description=description,color=color)

		self.add_all_cogs()

	def add_all_cogs(self):
		all_obj = [Analytics(self),NotificationSystem(self),VocalSalonSystem(self),BackupSystem(self),RolesSystem(self),DataBase(self),EditCommand(self),SendCommand(self),RenameVocalChannelCommand(self),PrivateVocalCommand(self),PublicVocalCommand(self)]
		for obj in all_obj:
			self.add_cog(obj)

	async def on_ready(self):
		await self.change_presence(activity=self.actv)
		print("[ ! Info ] Je suis prêt !\n=-----------------------=")


escarbot = Bot()
escarbot.run(config["BOT"]["TOKEN"])

