import datetime

from discord import TextChannel,utils
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
	async def on_component(self,ctx: ComponentContext):
		if str(ctx.custom_id) == "Rules_accepted":
			await self.edit_role("add",ctx.guild_id,self.bot.guilds_data[str(ctx.guild_id)]["roles"][0]["role_id"],ctx.author)
			return await ctx.send(content="Vous pouvez maintenant voir l'intégralité du serveur !",hidden=True)
		if ctx.selected_options is not None:
			for n,option in enumerate(ctx.selected_options):
				role = utils.get(ctx.guild.roles,id=int(option))
				if role is not None:
					await self.edit_role("add",ctx.guild_id,int(option),ctx.author)
				if n == len(ctx.selected_options)-1:
					return await ctx.send(content="Vous avez eu vos nouveau(x) rôle(s) !",hidden=True)

	@commands.Cog.listener()
	async def on_message(self,message):
		if message.author.bot is False:
			if isinstance(message.channel,TextChannel):
				year,month,day = str(datetime.datetime.today().date()).split("-")
				m = f"0{int(month)-1}" if int(month)-1 < 10 else month
				try:
					self.bot.users_data[str(message.guild.id)][str(message.author.id)]["NumberOfMessages"][f"{year}-{m}"]
				except KeyError:
					pass
				else:
					# Search regular role
					for n,role_database in enumerate(self.bot.guilds_data[str(message.guild.id)]["roles"]):
						if role_database["role_name"] == "regular":
							role = utils.get(message.guild.roles,id=int(role_database["role_id"]))
							break
						if int(n) == len(self.bot.guilds_data[str(message.guild.id)]["roles"])-1:
							return
					# If have regular role
					if 2500 < self.bot.users_data[str(message.guild.id)][str(message.author.id)]["NumberOfMessages"][f"{year}-{m}"]:
						return await message.author.add_roles(role)
					return await message.author.remove_roles(role)

