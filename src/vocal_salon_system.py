import datetime

from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions


class VocalSalonSystem(commands.Cog):
	""" VocalSalonSystem() -> Represent the creation of vocal custom with anyone ! """
	def __init__(self,bot):
		self.bot = bot
		self.last_channel_created = {}
		# Generic name for a vocal channel recently created
		self.generic_name = lambda name_member: f"{name_member}'s Channel."
		self.get_category = lambda guild,_id: utils.get(guild.categories,id=_id)

	async def create_vocal(self,guild,member):
		""" create_vocal() -> Create a channel when the member as joined "Crée un salon" """
		# Create and get the new vocal channel
		new_channel = await guild.create_voice_channel(self.generic_name(member.name),bitrate=64000,category=self.get_category(guild,self.bot.guilds_data[str(guild.id)]["categories_ID"]["vocals_channel"]))
		self.last_channel_created[member.id] = int(new_channel.id)
		# Log
		print(f"[{datetime.datetime.today().date()}] L'utilisateur {member.name} à crée un salon dans {guild.name} !")
		# Move the member to the vocal channel created
		await new_channel.edit(position=2)
		await member.move_to(new_channel)

	async def delete_vocal(self,before,member):
		""" delete_vocal() -> Delete a channel when the member as leave your channel """
		# If 0 as in channel
		if before.channel is not None:
			if (int(before.channel.id) == self.last_channel_created[member.id]) and (len(before.channel.members) == 0):
				# Log
				print(f"[{datetime.datetime.today().date()}] Le salon de {member.name} à été supprimé dans {member.guild.name} !")
				return await before.channel.delete()

	@commands.Cog.listener()
	@has_permissions(manage_channels=True)
	async def on_voice_state_update(self,member,before,after):
		if self.bot.guilds_data[str(member.guild.id)]["functions"]["create_personal_vocal"]:
			if (after.channel is not None) and (int(after.channel.id) == int(self.bot.guilds_data[str(member.guild.id)]["vocals_ID"]["create_vocal"])):
				return await self.create_vocal(member.guild,member)
			return await self.delete_vocal(before,member)
