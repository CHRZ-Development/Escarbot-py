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
		vocal_channel = utils.get(guild.voice_channels,id=int(self.bot.guilds_data[str(guild.id)]["messages_ID"]["stat"]))
		print(f"[{datetime.datetime.today().date()}] Le compteur de membre à étais actualisée, il affiche {self.title_members_channel(self.stats[guild.id]['all_members'])}")
		return await vocal_channel.edit(name=self.title_members_channel(self.stats[guild.id]["all_members"]))

	async def count_members(self,guild):
		""" count_members() -> Count all members in members role. """
		role_members = utils.get(guild.roles,id=int(self.bot.guilds_data[str(guild.id)]["roles"]["✅"]))
		self.stats[guild.id] = {"all_members": 0}
		self.stats[guild.id]["all_members"] = len(role_members.members)
		return await self.refresh_counter(guild)

	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.bot.guilds:
			if self.bot.guilds_data[str(guild.id)]["functions"]["stat"]:
				await self.count_members(guild)

	@commands.Cog.listener()
	async def on_member_join(self,member):
		if self.bot.guilds_data[str(member.guild.id)]["functions"]["stat"]:
			self.stats[member.guild.id]["all_members"] += 1 if not member.bot else 0
			await self.refresh_counter(member.guild)

	@commands.Cog.listener()
	async def on_member_remove(self,member):
		if self.bot.guilds_data[str(member.guild.id)]["functions"]["stat"]:
			self.stats[member.guild.id]["all_members"] -= 1 if not member.bot else 0
			await self.refresh_counter(member.guild)
