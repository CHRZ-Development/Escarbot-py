# -*- coding: UTF-8 -*-
import os
import json
import datetime

from typing import List
from discord.ext import commands
from discord import Colour,Embed,utils


class EditCommand(commands.Cog):
	""" EditCommand() -> Represent the edition of server setting and more. """
	def __init__(self,bot):
		self.bot = bot
		# DataBase directory
		self.guilds_data_path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
		self.edit_func = {"role_emoji": self.edit_role_emoji,"role_info": self.edit_role_info,"role": self.edit_role,"members_stat": self.edit_stat_members_channel,"rules_message": self.edit_rules_message,"create_personal_vocal": self.edit_create_vocal_channel,"function": self.edit_function,"nickname_member": self.edit_nickname_member}

	@staticmethod
	async def perm_check(ctx,roles_list: List[int]):
		""" perm_check() -> Check if the user who as executed a command have authorization. """
		for n,role in enumerate(ctx.author.roles):
			# If authorized
			if role.id in roles_list:
				return "pass"
			# Not authorized
			if n == len(ctx.author.roles)-1:
				return await ctx.send(embed=Embed(title="> **⚠ Attention !**",description="Vous n'avez pas la permission d'éxecutez cette commande !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))

	async def edit_role_emoji(self,ctx,args):
		""" edit_role_emoji() -> !edit role_emoji *args
			* It allow to edit an emoji has each role !
				:param args: role emoji | ex: member_role 👤 """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
			role,emoji = args
			guild_id = str(ctx.guild.id)
			self.bot.guilds_data[guild_id]["roles_emoji_reaction"][role] = emoji
			self.refresh_database()

	async def edit_role_info(self,ctx,args):
		""" edit_role_emoji() -> !edit role_info *args
			* It allow to edit an info has each role ! (For role attribute message)
				:param args: role info | ex: member_role "Default role" """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
			role,info = args
			self.bot.guilds_data[str(ctx.guild.id)]["roles_info"][role] = info
			self.refresh_database()

	async def edit_role(self,ctx,args):
		""" edit_role() -> !edit role *args
			* It allow to edit the role at an emoji ! (For role attribute message)
				:param args: emoji role_id | ex: 👤 852576991504105514 """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
			emoji,role_id = args
			self.bot.guilds_data[str(ctx.guild.id)]["roles"][emoji] = int(role_id)
			self.refresh_database()

	async def edit_stat_members_channel(self,ctx,args):
		""" edit_stat_members_channel() -> !edit members_stat *args
			* It allow to edit the channel which display the members total stat in a guild !
				:param args: vocal_id | ex: 852576991504105514 """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
			guild_id = str(ctx.guild.id)
			self.bot.guilds_data[guild_id]["messages_ID"]["stat"] = int(args[0])
			self.refresh_database()

	async def edit_rules_message(self,ctx,args):
		""" edit_rules_message() -> !edit rules_message *args
			* It allow to edit the little verification message function on the server when he/she join this one !
				:param args: message_id | ex: 852576991504105514 """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
			guild_id = str(ctx.guild.id)
			self.bot.guilds_data[guild_id]["messages_ID"]["rules"] = int(args[0])
			self.refresh_database()

	async def edit_create_vocal_channel(self,ctx,args):
		""" edit_create_vocal_channel() -> !edit create_vocal_channel *args
			* It allow to edit id channel custom !
				:param args: vocal_id | ex: 852576991504105514 """
		# Always owner can execute this command
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
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
		perm_check = await self.perm_check(ctx,self.bot.guilds_data[str(ctx.guild.id)]["role_perm_command"]["nickname_member"])
		if perm_check == "pass":
			member_id,member_name = args
			member = utils.get(ctx.guild.members,id=int(member_id))
			# Log
			print(f"[{datetime.datetime.today().date()}] L'utilisateur {ctx.author.name} à modifié le pseudo de {member.display_name} par {member_name}")
			return await member.edit(nick=member_name)

	async def edit_function(self,ctx,args):
		""" edit_function() -> !edit function *args
			* It allow to enable or disable a function !
				:param args: function_name bool | ex: stat False """
		perm_check = await self.perm_check(ctx,[ctx.guild.owner.roles[len(ctx.guild.owner.roles)-1].id])
		if perm_check == "pass":
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
	async def edit_command(self,ctx,option,*args):
		""" edit_command() -> !edit
			* It allow to edit settings the server and more """
		try:
			await self.edit_func[option](ctx,args)
		except KeyError:
			return await ctx.send(embed=Embed(title="> **⚠ Attention !**",description="Cette commande n'existe ou verifié l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
		await ctx.message.delete()

