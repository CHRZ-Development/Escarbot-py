import datetime

from discord import utils
from discord.ext import commands
from discord_slash import ComponentContext


class RolesSystem(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

	async def edit_role(self,option,guild_id,role_id,member):
		guild = utils.get(self.bot.guilds,id=int(guild_id))
		role = utils.get(guild.roles,id=int(role_id))
		return await member.add_roles(role) if option == "add" else await member.remove_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self,event):
		if event.member.bot is False:
			# What message ?
			for key in self.bot.guilds_data[str(event.guild_id)]["messages_ID"]:
				# If two ID is the same.
				if int(event.message_id) == int(self.bot.guilds_data[str(event.guild_id)]["messages_ID"][key]):
					# Attribute role
					return await self.edit_role("add",event.guild_id,self.bot.guilds_data[str(event.guild_id)]["roles"][str(event.emoji)],event.member)

	@commands.Cog.listener()
	async def on_component(self,ctx: ComponentContext):
		if str(ctx.custom_id) == "Rules_accepted":
			return await self.edit_role("add",ctx.guild_id,self.bot.guilds_data[str(ctx.guild_id)]["roles"]["✅"],ctx.author)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self,event):
		# Get member who as remove a reaction
		guild = utils.get(self.bot.guilds,id=event.guild_id)
		member = utils.get(guild.members,id=event.user_id)

		if member is not None:
			if member.bot is False:
				# What message ?
				for key in self.bot.guilds_data[str(event.guild_id)]["messages_ID"]:
					# If two ID is the same.
					if int(event.message_id) == int(self.bot.guilds_data[str(event.guild_id)]["messages_ID"][key]):
						# Remove role
						return await self.edit_role("remove",event.guild_id,self.bot.guilds_data[str(event.guild_id)]["roles"][str(event.emoji)],member)

	@commands.Cog.listener()
	async def on_message(self,message):
		year,month,day = str(datetime.datetime.today().date()).split("-")
		if int(month)-1 < 10:
			m = f"0{int(month)}"
		else:
			m = month
		try:
			self.bot.users_data[str(message.guild.id)][str(message.author.id)]["NumberOfMessages"][f"{year}-{int(m)-1}"]
		except KeyError:
			pass
		else:
			try:
				role = utils.get(message.guild.roles,id=int(self.bot.guilds_data[str(message.guild.id)]["roles"]["📅"]))
			except KeyError:
				pass
			else:
				if 3500 < self.bot.users_data[str(message.guild.id)][str(message.author.id)]["NumberOfMessages"][f"{year}-{int(m)-1}"] < 5000:
					await message.author.add_roles(role)
				else:
					await message.author.remove_roles(role)

