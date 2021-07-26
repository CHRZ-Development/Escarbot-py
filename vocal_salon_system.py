from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions


class VocalSalonSystem(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.last_channel_created = {}

		self.vocal_category_id = 841302654588026940

	async def create_vocal(self,guild,member):
		category = utils.get(guild.categories,id=self.vocal_category_id)
		name_channel = f'{member.name} Channel'
		new_channel = await guild.create_voice_channel(name_channel,bitrate=64000,category=category)
		self.last_channel_created[member.id] = int(new_channel.id)

		await new_channel.edit(position=2)
		await member.move_to(new_channel)

	async def delete_vocal(self,after,before,member):
		if (before.channel is not None) and (after.channel is None):
			if (int(before.channel.id) == self.last_channel_created[member.id]) and (len(before.channel.members) == 0):
				return await before.channel.delete()

	@commands.Cog.listener()
	@has_permissions(manage_channels=True)
	async def on_voice_state_update(self,member,before,after):
		ids = self.bot.ids[member.guild.id]
		guild = utils.get(self.bot.guilds,id=member.guild.id)

		if (after.channel is not None) and (after.channel.id == ids["id_vocal_channel_create"]):
			return await self.create_vocal(guild,member)
		return await self.delete_vocal(after,before,member)
