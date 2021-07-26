import datetime
import os

from discord import utils
from discord.ext import commands


class DataBase(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

		self.date_index = {0: 'Year',1: 'Month',2: 'Day'}

	def create_data_user(self,m_id):
		""" create_data_user( ) -> Create a database for a new user.
				:param m_id: Member ID """
		for guild in self.bot.guilds:
			# Get member
			member = utils.get(guild.members,id=int(m_id))
			d,m,y = str(datetime.date.today()).split('-')
			date,hours = str(member.joined_at).split(' ')

			# Load data base
			data = self.bot.file.load('data.json')
			# Create data for new user
			data[m_id] = self.bot.template
			data[m_id]['KickFunction'] = {'Day': d,'Month': m,'Year': y}

			for n,slot in enumerate(date.split('-')):
				data[member.id]['JoinedAt'][self.date_index[n]] = slot

			parent_dir = 'DataPerUser'
			new_dir = str(m_id)
			try:
				# Path access
				path = os.path.join(parent_dir,new_dir)
				# Make a new directory for data.json file
				os.mkdir(path)
			except OSError:
				pass
			self.bot.file.write(data,'data.json')

	def delete_data_user(self,m):
		""" delete_data_user( ) -> Delete the database when a user at leave the server.
				:param m: Member """
		if m.bot is False:
			data = self.bot.file.load('data.json')
			# Delete the user in data base
			data.pop(m.name)
			# Write new data base actualized
			self.bot.file.write(data,'data.json')

	@commands.Cog.listener()
	async def on_member_join(self,member):
		self.create_data_user(member.id)

	@commands.Cog.listener()
	async def on_remove_remove(self,member):
		self.delete_data_user(member)
