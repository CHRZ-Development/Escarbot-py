from typing import Optional
from discord import Colour
from discord.ext import commands
from scripts import is_owner


class EditCommand(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.check( is_owner )
	@commands.command( name= 'edit' )
	async def edit_custom( self, ctx, type: str, id: int, title: str, description: Optional[ str ], color: Optional[ Colour ] ):
		message = ctx.channel.get_partial_message( id )

		await message.edit( embed = self.bot.create_embed( title, description, color ) ) if type == 'embed' else None
		await message.edit( content = title ) if type == 'normal' else None
