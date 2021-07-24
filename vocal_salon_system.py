from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions


class VocalSalonSystem( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot
		self.last_channel_created = {}

	@commands.Cog.listener()
	@has_permissions( manage_channels= True )
	async def on_voice_state_update(self, member, before, after):
		ids = self.bot.ids[member.guild.id]
		guild = utils.get( self.bot.guilds, id= member.guild.id )
		categorie = utils.get( guild.categories, id= 841302654588026940 )

		if (after.channel is not None) and (after.channel.id == ids["id_vocal_channel_create"]):
			name_channel = f'{member.name} Channel'
			new_channel = await guild.create_voice_channel(name_channel, bitrate= 64000, category= categorie)
			await new_channel.edit(position= 2)
			self.last_channel_created[member.id] = new_channel.id
			await member.move_to( new_channel )
		else:
			if after.channel is None:
				if (before.channel.id == self.last_channel_created[member.id]) and (len(before.channel.members) == 0):
					return await before.channel.delete()
			else:
				if after.channel.id != before.channel.id:
					if (before.channel.id == self.last_channel_created[member.id]) and (len(before.channel.members) == 0):
						return await before.channel.delete()
