from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
import configparser, os, datetime


class Analytics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		__config = configparser.ConfigParser()
		__config.read(os.path.join('res/', 'cfg.ini'))

		self.stats = {}
		__template = {"all_members": 0, "all_messages": 0}

		self.user_data_file = "user_data.json"
		self.user_data_dir = f"{os.getcwd()}/res/"

		for guild in self.bot.guilds:
			self.stats[guild.id] = __template

		self.title_members_channel = lambda all_members: f"👤｜{all_members}・𝘔𝘦𝘮𝘣𝘳𝘦𝘴"

	def count_messages(self):
		""" count_messages( ) -> count all messages in all servers for analytics """
		data = self.bot.file.load(self.user_data_file, self.user_data_dir)

		for guild in self.bot.guilds:
			# Reset
			self.stats[guild.id]["all_messages"] = 0
			# Count all messages
			for date_key in data['NumberOfMessages']:
				self.stats[guild.id]["all_messages"] += int(data['NumberOfMessages'][date_key])

	@has_permissions(manage_channels=True)
	async def count_members(self):
		""" count_members() -> Count all members in members role. """
		for guild in self.bot.guilds:
			channel_members = self.bot.get_channel(self.bot.ids[guild.id]["id_channel_members"])
			role_members = utils.get(guild.roles, id=self.bot.ids[guild.id]['id_role_default'])
			self.stats[guild.id]["all_members"] = len(role_members.members)
			# Edit display stat
			await channel_members.edit(name=self.title_members_channel(self.stats[guild.id]["all_members"]))

	def add_counter_messages(self, m):
		""" add_counter_messages( ) -> Add 1 every time of one message as been sending
				:param m: Member """
		if m.author.bot is False:
			y, month, d = str(datetime.date.today()).split('-')
			# Getting the guild where the member is situated
			guild = utils.get(self.bot.guilds, id= m.guild.id)

			data = self.bot.file.load(self.user_data_file, self.user_data_dir)
			key_data = f'{y}-{month}'
			# Add 1 to the counters
			try:
				# Global counter | User counter
				data['NumberOfMessages'][key_data] += 1
				data[m.author.name]['NumberOfMessages'][key_data] += 1
			except KeyError:
				# Add new date key in global counter and user
				data['NumberOfMessages'][key_data] = 1
				data[m.author.name]['NumberOfMessages'][key_data] = 1
			self.stats[guild.id]["all_messages"] += 1

			self.bot.file.write(data, self.user_data_file, self.user_data_dir)

	@commands.Cog.listener()
	async def on_message(self, message):
		self.add_counter_messages(message)

	@commands.Cog.listener()
	async def on_ready(self):
		await self.count_members()
		self.count_messages()

