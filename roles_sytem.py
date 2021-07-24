from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions


class RolesSystem(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		self.get_role = lambda guild, id_role: utils.get( guild.roles, id= id_role )

	@has_permissions(manage_messages=True, manage_roles=True)
	async def attribute_role(self, e, c_id):
		role = self.check_reactions(e, c_id)

		if role is None:
			channel = self.bot.get_channel(e.channel_id)
			message = channel.get_partial_message(e.message_id)
			return await message.clear_reaction(str(e.emoji.name))
		for str_role in self.bot.attribute_index[e.guild_id]:
			if role == str_role:
				guild = utils.get(self.bot.guilds, id=e.guild_id)
				return await e.member.add_roles(self.get_role(guild, self.bot.attribute_index[e.guild_id][role]))

	@has_permissions(manage_messages=True, manage_roles=True)
	async def remove_role(self, e):
		guild = utils.get(self.bot.guilds, id=e.guild_id)
		member = utils.get(guild.members, id=int(e.user_id))

		for m_id in self.bot.roles_index[guild.id]:
			# Attribute role
			if (int(e.message_id) == m_id) and (str(e.emoji) == self.bot.emoji_check):
				role = self.bot.roles_index[guild.id][m_id]
				guild = utils.get(self.bot.guilds, id=e.guild_id)
				await member.remove_roles(self.get_role(guild, self.bot.attribute_index[guild.id][role]))
				break

	def check_reactions( self, e, c_id ):
		if int( e.channel_id ) == c_id:
			if str( e.emoji ) == self.bot.emoji_check:
				# If the user set a other emoji on reaction
				for m_id in self.bot.roles_index[ e.guild_id ]:
					# Attribute role
					if int( e.message_id ) == int( m_id ):
						return self.bot.roles_index[ e.guild_id ][ m_id ]
			return None

	async def send_welcome(self, m):
		""" send_welcome( ) -> Send a welcome message for a new member
				:param m: Member """
		guild = utils.get(self.bot.guilds, id = m.guild.id)

		welcome_channel = self.bot.get_channel(self.bot.ids[guild.id]['id_channel_welcome'])
		await welcome_channel.send(embed = self.bot.create_embed("> __**Bienvenue !**__", f"_ _\n👋 Je te souhaite la bienvenue {m.mention} !\n_ _", 0xff8000))

	@commands.Cog.listener()
	@has_permissions(manage_roles= True)
	async def on_raw_reaction_add(self, event):
		ids = self.bot.ids[event.guild_id]

		# Attribute roles
		if event.channel_id == ids['id_channel_rules']:
			return await self.attribute_role(event, ids['id_channel_rules']), await self.send_welcome(event.member)
		elif event.channel_id == ids['id_channel_roles']:
			return await self.attribute_role(event, ids['id_channel_roles'])

	@commands.Cog.listener()
	@has_permissions(manage_messages=True, manage_roles=True)
	async def on_raw_reaction_remove(self, event):
		ids = self.bot.ids[event.guild_id]

		await self.remove_role(event) if event.channel_id == ids['id_channel_roles'] else None
