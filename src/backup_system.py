import os
import time

from discord.ext import commands
from discord.ext.tasks import loop


class BackupSystem(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.last_date_edited = {'Day': 12,'Month': 7,'Year': 2021}

	def backup_file(self):
		path = f'{os.getcwd()}/res/user_data.json'
		# Convert seconds since epoch to Date only
		modification_time = time.strftime('%d-%m-%Y',time.localtime(os.path.getmtime(path)))
		file_d,file_m,file_y = modification_time.split('-')
		self.bot.file.copy(f'{os.getcwd()}/res/','user_data.json',f'{os.getcwd()}/BackupData/') if (int(file_d) != self.last_date_edited['Day']) or (int(file_m) != self.last_date_edited['Month']) or (int(file_y) != self.last_date_edited['Year']) else None
		self.last_date_edited['Day'] = file_d
		self.last_date_edited['Month'] = file_m
		self.last_date_edited['Year'] = file_y

	@loop(minutes=15)
	async def check_need_backup(self):
		await self.bot.wait_until_ready()
		self.backup_file()

	@commands.Cog.listener()
	async def on_ready(self):
		await self.check_need_backup.start()
