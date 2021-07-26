from discord.ext import commands
from discord import PermissionOverwrite
from discord.ext.commands import has_permissions


def set_permissions():
	perms = PermissionOverwrite()
	perms.manage_channels = True
	perms.manage_roles = True
	perms.connect = True
	return perms


class RenameVocalChannelCommand(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name= 'rename')
	@has_permissions(manage_channels=True, manage_roles=True)
	async def rename_vocal_channel(self, ctx, name):
		vocal_channel = ctx.author.voice

		if vocal_channel is not None:
			vocal_channel = ctx.author.voice.channel
			if vocal_channel.id not in [841962121838592000, 868284742846533672]:

				await vocal_channel.set_permissions(ctx.author, overwrite= set_permissions())
				await vocal_channel.edit(name= name)
