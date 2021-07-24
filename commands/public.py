from discord import PermissionOverwrite, utils
from discord.ext import commands
from discord.ext.commands import has_permissions


class PublicVocalCommand( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot

	@commands.command( name= 'public' )
	@has_permissions( manage_channels= True, manage_roles= True )
	async def make_public_vocal(self, ctx):
		vocal_channel = ctx.author.voice.channel

		if vocal_channel is not None:
			if vocal_channel.id not in [841962121838592000, 868284742846533672]:
				everyone = utils.get( ctx.author.guild.roles, id= 838862631284506705 )
				overwrite = PermissionOverwrite()
				overwrite.connect = True
				await vocal_channel.set_permissions(everyone, overwrite= overwrite)

