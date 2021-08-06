from http.client import HTTPException
from discord import utils,Forbidden,Member
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.tasks import loop

from APIs.twitch import TwitchAPI
from APIs.youtube import YouTubeAPI


class NotificationSystem(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.msg_booster = lambda a: f"😁 **Merci !** {a.mention} **d'avoir boost le serveur !** ❤ \nhttps://media.giphy.com/media/3oEdva9BUHPIs2SkGk/giphy.gif "

		self.youtube_api = YouTubeAPI(self.bot)
		self.youtube_api.create()
		self.twitch_api = TwitchAPI(self.bot)
		self.twitch_api.create()

	async def send_invitation(self,m):
		""" send invitation( ) -> Send a invitation in message private
				:param m: Member """
		return await m.send(embed=self.bot.create_embed("> **AventuraBuild**","https://discord.gg/H3vtCv9Nw9",0xff8000))

	async def detect_role_changed(self,b,a):
		""" detect_role_changed( ) -> Notify hierarchical change
				:param b: before
				:param a: after """
		b_role,a_role = {},{}
		# Text Channel
		channel_lvlup = self.bot.get_channel(self.bot.ids[a.guild.id]["id_channel_lvlup"])

		# If the roles at been changed
		if a.roles != b.roles:
			# Write all role between after and before role attribute
			number_keys_b_role,number_keys_a_role = 0,0
			for role in b.roles:
				b_role[role.name] = role
				number_keys_b_role += 1
			for role in a.roles:
				a_role[role.name] = role
				number_keys_a_role += 1
			# If after attribute role as been changed
			if number_keys_a_role > number_keys_b_role:
				change_role = a_role
				compare_role = b_role
			else:
				# Stop this function
				return False
			# Detect the new name of role
			role_update = None
			for role in change_role:
				try:
					compare_role[role].items()
				except KeyError:
					role_update = role
			try:
				# Send the hierarchical changed
				return await channel_lvlup.send(embed=self.bot.create_embed("> __**Niveau superieurs !**__",f"_ _\n**Vous avez eu un niveau superieurs** {a.mention} ! Vous avez maintenant {role_update}.\n_ _",0x00ff40))
			except (Forbidden,HTTPException):
				pass

	@has_permissions(manage_roles=True)
	async def check_user_booster(self,b: Member,a: Member):
		if b.premium_since == a.premium_since:
			return False

		guild = utils.get(self.bot.guilds,id=a.guild_id)
		if a.premium_since is None:
			return await a.remove_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))

		channel_lvlup = self.bot.get_channel(self.bot.ids[a.guild.id]["id_channel_lvlup"])
		await a.add_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))
		await channel_lvlup.send(embed=self.bot.create_embed("> __**Wow !**__",f"_ _\n**Merci** {a.mention} **d'avoir boost le serveur !** ❤ ! Vous avez maintenant accès à des avantages !\n_ _",0xff80c0))

	@commands.Cog.listener()
	@has_permissions(manage_messages=True,manage_roles=True)
	async def on_raw_reaction_add(self,event):
		ids = self.bot.ids[event.guild_id]

		# Send Discord invitation
		if event.guild_id == self.bot.chrz_development:
			if event.channel_id == ids['id_channel_minecraft']:
				if event.emoji.name == self.bot.emoji_check:
					return await self.send_invitation(event.member)
				channel = self.bot.get_channel(event.channel_id)
				message = channel.get_partial_message(event.message_id)
				return await message.clear_reaction(str(event.emoji.name))

	@commands.Cog.listener()
	async def on_member_update(self,before,after):
		# Send and mentioned the user of role as been changed
		await self.detect_role_changed(before,after)
		await self.check_user_booster(before,after)

	@commands.Cog.listener()
	async def on_ready(self):
		self.youtube_api.append_videos_ids()
		await self.api_event.start()

	@loop(minutes=1)
	async def api_event(self):
		await self.bot.wait_until_ready()
		await self.youtube_api.video_notification_system()
		await self.twitch_api.live_notification_system()
