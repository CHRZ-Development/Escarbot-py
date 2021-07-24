# -*- coding: UTF-8 -*-
# https://discord.gg/yEvBg8CPaM
# https://www.youtube.com/channel/UCbl4AHVket_DNhBzQG56f7w
from discord import (Intents, Embed)
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
import os, configparser


# Permissions
i = Intents.all()
i.presences = True
i.members = True
i.messages = True
i.guilds = True
i.guild_messages = True
i.guild_reactions = True
i.reactions = True
i.voice_states = True

config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/res/cfg.ini')


class Bot(commands.Bot):

	def __init__(self):
		commands.Bot.__init__(self, command_prefix='!', intents=i)

		# ID Guilds
		self.chrz_development = 838862631284506705
		self.aventurabuild = 846458770963169360
		self.emoji_check = "✅"
		self.actv = Activities(version=config["BOT"]["version"])

		self.file = FileManager()
		guilds_data = self.file.load(f'{os.getcwd()}/res/guilds_data.json')
		self.roles_index = {838862631284506705: guilds_data["838862631284506705"]["roles_index"],
						    846458770963169360: guilds_data["846458770963169360"]["roles_index"]}
		self.attribute_index = {838862631284506705: guilds_data["838862631284506705"]["attribute_index"],
			                    846458770963169360: guilds_data["846458770963169360"]["attribute_index"]}
		self.ids = {838862631284506705: guilds_data["838862631284506705"]["ids"],
			        846458770963169360: guilds_data["846458770963169360"]["ids"]}

		# Title text channel
		self.title_members_channel = lambda all_members: f"👤｜{all_members}・𝘔𝘦𝘮𝘣𝘳𝘦𝘴"
		# Messages
		self.create_embed = lambda title, description, color: Embed(title=title, description=description, color=color)

	async def on_ready(self):
		print("Je me lance, veuillez patientez...")

		analytics_system = Analytics(self)
		notif_system = NotificationSystem(self)
		vocal_salon_system = VocalSalonSystem(self)
		backup_system = BackupSystem(self)
		roles_system = RolesSystem(self)
		database_refresh = DataBase(self)
		edit_command = EditCommand(self)
		send_command = SendCommand(self)
		rename_command = RenameVocalChannelCommand(self)
		private_command = PrivateVocalCommand(self)
		public_command = PublicVocalCommand(self)

		self.add_cog(analytics_system)
		self.add_cog(notif_system)
		self.add_cog(backup_system)
		self.add_cog(roles_system)
		self.add_cog(vocal_salon_system)
		self.add_cog(database_refresh)
		self.add_cog(edit_command)
		self.add_cog(send_command)
		self.add_cog(rename_command)
		self.add_cog(private_command)
		self.add_cog(public_command)

		await self.change_presence(activity= self.actv)

		print("[ ! Info ] Je suis prêt !\n=-----------------------=")

	async def on_message(self, message):
		await self.process_commands(message)


__escarbot = Bot()
# Start bot
__escarbot.run(config["BOT"]["TOKEN"])
