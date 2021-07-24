from typing import Optional
from discord import Colour
from discord.ext import commands
from scripts import is_owner


class SendCommand(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.check( is_owner )
	@commands.command( name= 'send' )
	async def send_custom( self, ctx, type: str, title: str, description: Optional[ str ], color: Optional[ Colour ] ):
		await ctx.send( embed = self.bot.create_embed( title, description, color ) ) if type == 'embed' else None
		await ctx.send( content = title ) if type == 'normal' else None

