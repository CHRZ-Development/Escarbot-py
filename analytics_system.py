import configparser
import os

from discord import utils
from discord.ext import commands


class Analytics(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

		__config = configparser.ConfigParser()
		__config.read(os.path.join('res/','cfg.ini'))

		self.stats = {}
		self.__template = {"all_members": 0}

		self.user_data_file = "user_data.json"
		self.user_data_dir = f"{os.getcwd()}/res/"

		self.title_members_channel = lambda all_members: f"👤｜{all_members}・𝘔𝘦𝘮𝘣𝘳𝘦𝘴"

	async def count_members(self):
		""" count_members() -> Count all members in members role. """
		for guild in self.bot.guilds:
			channel_members = self.bot.get_channel(self.bot.ids[guild.id]["id_channel_members"])
			role_members = utils.get(guild.roles,id=self.bot.ids[guild.id]['id_role_default'])
			self.stats[guild.id] = self.__template
			self.stats[guild.id]["all_members"] = len(role_members.members)  # Edit display stat

			await channel_members.edit(name=self.title_members_channel(self.stats[guild.id]["all_members"]))

	@commands.Cog.listener()
	async def on_ready(self):
		await self.count_members()
