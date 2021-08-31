import datetime

from discord import utils
from discord.ext import commands


class Analytics(commands.Cog):
	""" Analytics() -> Represent all analytic which can be displayed. """
	def __init__(self,bot):
		self.bot = bot
		self.stats = {}
		self.title_members_channel = lambda all_members: f"👤｜{all_members}・𝘔𝘦𝘮𝘣𝘳𝘦𝘴"

	async def refresh_counter(self,guild):
		""" refresh_counter() -> Refresh the vocal channel title which display the stat. """
		for channel_database in self.bot.guilds_data[str(guild.id)]["channels"]:
			if channel_database["function"] in ["members_counter"]:
				vocal_channel = utils.get(guild.voice_channels,id=int(channel_database["channel_id"]))
				await vocal_channel.edit(name=f"👤｜{self.stats[guild.id]['all_members']}・𝘔𝘦𝘮𝘣𝘳𝘦𝘴")
				print(f"[{datetime.datetime.today().date()}] Le compteur de membre à étais actualisée, il affiche {self.title_members_channel(self.stats[guild.id]['all_members'])} dans {guild.name}")
				break

	async def count_members(self,guild):
		""" count_members() -> Count all members in members role. """
		self.stats[guild.id] = {"all_members": 0}
		try:
			role_members = utils.get(guild.roles,id=int(self.bot.guilds_data[str(guild.id)]["roles"][0]["role_id"]))
		except IndexError:
			return
		for member in role_members.members:
			if member.bot is False:
				self.stats[guild.id]["all_members"] += 1

	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.bot.guilds:
			try:
				self.bot.guilds_data[str(guild.id)]["channels"]
			except KeyError:
				pass
			else:
				for channel_database in self.bot.guilds_data[str(guild.id)]["channels"]:
					if channel_database["function"] in ["members_counter"]:
						await self.count_members(guild)
						await self.refresh_counter(guild)

	@commands.Cog.listener()
	async def on_member_join(self,member):
		for channel_database in self.bot.guilds_data[str(member.guild.id)]["channels"]:
			if channel_database["function"] in ["members_counter"]:
				self.stats[member.guild.id]["all_members"] += 1 if not member.bot else 0
				await self.refresh_counter(member.guild)

	@commands.Cog.listener()
	async def on_member_remove(self,member):
		for channel_database in self.bot.guilds_data[str(member.guild.id)]["channels"]:
			if channel_database["function"] in ["members_counter"]:
				self.stats[member.guild.id]["all_members"] -= 1 if not member.bot else 0
				await self.refresh_counter(member.guild)
