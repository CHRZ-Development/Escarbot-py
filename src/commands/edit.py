# -*- coding: UTF-8 -*-
import os
import json
import datetime

from discord.ext import commands
from discord import Colour,Embed,utils

from src.exceptions.InvalidEditRoleSection import InvalidEditRoleSection
from src.exceptions.InvalidSubcommand import InvalidSubcommand


class EditCommand(commands.Cog):
	""" EditCommand() -> Represent the edition of server setting and more. """
	def __init__(self,bot):
		self.bot = bot
		# DataBase directory
		self.guilds_data_path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
		self.edit_func = {"channel": self.edit_channel,"role": self.edit_role,"members_stat": self.edit_stat_members_channel,"create_personal_vocal": self.edit_create_vocal_channel,"function": self.edit_function,"nickname_member": self.edit_nickname_member}
		self.edit.add_check(self.bot.check_permission)

	async def edit_role(self,ctx,args):
		""" edit_role() -> !edit role *args
			* It allow to edit the role at an emoji ! (For role attribute message)
				:param args: role_id <option> <edit_value> | ex: 852576991504105514 can_execute_command "ping,mute" """
		for n,role_database in enumerate(self.bot.guilds_data[str(ctx.guild.id)]["roles"]):
			if role_database["role_id"] == args[0]:
				if args[1] in ["can_execute_command","role_name","role_id","emoji","info"]:
					if args[1] == "can_execute_command":
						self.bot.guilds_data[str(ctx.guild.id)]["roles"][n][args[1]] = str(args[2]).split(",")
						return
					self.bot.guilds_data[str(ctx.guild.id)]["roles"][n][args[1]] = args[2]
					return self.refresh_database()
				raise InvalidEditRoleSection(args[1])

	async def edit_channel(self,ctx,args):
		for n,channel_database in enumerate(self.bot.guilds_data[str(ctx.guild.id)]["channels"]):
			if channel_database["channel_id"] == args[0]:
				if args[1] in ["function","channel_name","channel_id","category_id","info"]:
					self.bot.guilds_data[str(ctx.guild.id)]["channels"][n][args[1]] = args[2]
					return self.refresh_database()

	async def edit_stat_members_channel(self,ctx,args):
		""" edit_stat_members_channel() -> !edit members_stat *args
			* It allow to edit the channel which display the members total stat in a guild !
				:param args: vocal_id | ex: 852576991504105514 """
		# Always owner can execute this command
		guild_id = str(ctx.guild.id)
		self.bot.guilds_data[guild_id]["messages_ID"]["stat"] = int(args[0])
		self.refresh_database()

	async def edit_create_vocal_channel(self,ctx,args):
		""" edit_create_vocal_channel() -> !edit create_vocal_channel *args
			* It allow to edit id channel custom !
				:param args: vocal_id | ex: 852576991504105514 """
		# Always owner can execute this command
		guild_id = str(ctx.guild.id)
		vocal_id = args[0]
		vocal_channel = utils.get(ctx.guild.voice_channels,id=int(vocal_id))
		# Enable the functionality
		self.bot.guilds_data[guild_id]["vocals_ID"]["create_vocal"] = int(vocal_id)
		self.bot.guilds_data[guild_id]["categories_ID"]["vocals_channel"] = int(vocal_channel.category_id)
		self.refresh_database()

	async def edit_nickname_member(self,ctx,args):
		""" edit_nickname_member() -> !edit nickname_member *args
			* It allow to edit a nickname to a member.
				:param args: user_id new_nickname | ex: 764219613231185930 "New nickname" """
		member_id,member_name = args
		member = utils.get(ctx.guild.members,id=int(member_id))
		# Log
		print(f"[{datetime.datetime.today().date()}] L'utilisateur {ctx.author.name} à modifié le pseudo de {member.display_name} par {member_name}")
		return await member.edit(nick=member_name)

	async def edit_function(self,ctx,args):
		""" edit_function() -> !edit function *args
			* It allow to enable or disable a function !
				:param args: function_name bool | ex: stat False """
		_function,_bool = args
		try:
			self.bot.guilds_data[ctx.guild.id]["functions"][_function] = bool(_bool)
		except KeyError:
			return await ctx.send(embed=Embed(title="> **⚠ Attention !**",description="Cette commande n'existe ou verifié l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
		self.refresh_database()

	def refresh_database(self):
		with open(self.guilds_data_path,"w") as f:
			json.dump(self.bot.guilds_data,f)

	@commands.command(name='edit')
	async def edit(self,ctx,option,*args):
		""" edit_command() -> !edit
			* It allow to edit settings the server and more """
		try:
			await self.edit_func[option](ctx,args)
		except KeyError:
			raise InvalidSubcommand(option)
		await ctx.message.delete()
