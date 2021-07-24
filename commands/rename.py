from discord.ext import commands
from discord.ext.commands import has_permissions


class RenameVocalChannelCommand(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name= 'rename')
	@has_permissions(manage_channels = True)
	async def rename_vocal_channel(self, ctx, name):
		vocal_channel = ctx.author.voice.channel

		if vocal_channel is not None:
			if vocal_channel.id not in [841962121838592000, 868284742846533672]:
				await vocal_channel.edit(name= name)
