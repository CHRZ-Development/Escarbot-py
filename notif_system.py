from http.client import HTTPException
from typing import Any
from discord import utils,Forbidden,Member
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.tasks import loop
from twitchAPI import Twitch,TwitchAPIException,TwitchBackendException
import google_auth_oauthlib.flow,googleapiclient.discovery,os,httplib2,configparser


class NotificationSystem(commands.Cog):
	twitch: Twitch
	youtube: Any

	def __init__(self,bot):
		self.bot = bot

		__path = os.path.join('res/','cfg.ini')
		__config = configparser.ConfigParser()
		__config.read(__path)

		self.app_id = __config["TWITCH"]["app_id"]
		self.app_secret = __config["TWITCH"]["app_secret"]
		self.channel_id = __config["YOUTUBE"]["channel_id"]
		self.api_service_name = __config["BOT"]["api_service_name"]
		self.api_version = __config["BOT"]["api_version"]
		self.client_secrets_file = __config["BOT"]["client_secrets_file"]
		self.scopes = [__config["BOT"]["scopes"]]

		self.id_all_videos = []
		self.all_streams = [00000000000]

		self.msg_booster = lambda a: f"😁 **Merci !** {a.mention} **d'avoir boost le serveur !** ❤ \nhttps://media.giphy.com/media/3oEdva9BUHPIs2SkGk/giphy.gif "

		self.create_twitch_api()
		self.create_youtube_api()

	def create_youtube_api(self):
		os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secrets_file,self.scopes)
		credentials = flow.run_console()
		self.youtube = googleapiclient.discovery.build(self.api_service_name,self.api_version,credentials=credentials)

	def create_twitch_api(self):
		# create instance of twitch API
		self.twitch = Twitch(self.app_id,self.app_secret)
		self.twitch.authenticate_app([])
		# get ID of user
		user_info = self.twitch.get_users(logins=['NaulaN_CHRZdev'])
		self.user_id = user_info['data'][0]['id']

	def requests_youtube(self,max_r=1,p="snippet,contentDetails,id"):
		""" request_youtube( ) -> Send a request to youtube for will get a new videos. """
		request = self.youtube.activities().list(part=p,channelId=self.channel_id,maxResults=max_r)
		try:
			response = request.execute()
			return response
		except httplib2.error.ServerNotFoundError:
			pass

	def request_twitch(self):
		""" request_twitch( ) -> Send a request to twitch for will get a new live """
		# Check if stream
		try:
			stream = self.twitch.get_streams(user_id=self.user_id,first=1)
			return stream
		except (TwitchAPIException,TwitchBackendException):
			pass

	async def send_invitation(self,m):
		""" send invitation( ) -> Send a invitation in message private
				:param m: Member """
		return await m.send(embed=self.bot.create_embed("> **AventuraBuild**","https://discord.gg/H3vtCv9Nw9",0xff8000))

	async def send_video_notification(self,r):
		chrz_development = utils.get(self.bot.guilds,id=838862631284506705)
		videos_role = utils.get(chrz_development.roles,id=self.bot.ids[chrz_development.id]['id_role_notify_videos'])

		channel_videos = self.bot.get_channel(self.bot.ids[chrz_development.id]['id_channel_videos'])
		self.last_video = r["items"][0]["snippet"]["title"]
		await channel_videos.send(content=f'{videos_role.mention}\n>  **Oh ! __{r["items"][0]["snippet"]["channelTitle"]}__ à publié une __nouvelle vidéo__ !** \n👍 + 💬 + 🔔 = ✅ Merciii !\nhttps://youtu.be/{r["items"][0]["contentDetails"]["upload"]["videoId"]}')

	async def send_twitch_notification(self,s):
		chrz_development = utils.get(self.bot.guilds,id=838862631284506705)
		live_role = utils.get(chrz_development.roles,id=self.bot.ids[chrz_development.id]['id_role_notify_live'])

		channel_live = self.bot.get_channel(self.bot.ids[chrz_development.id]['id_channel_live'])
		await channel_live.send(content=f'{live_role.mention}\n>  **Tien Tien Tien, {s["data"][0]["user_name"]} stream** "{s["data"][0]["title"]}" **actuellement !**\n https://www.twitch.tv/naulan_chrzdev ')

	async def video_youtube_notification_system(self):
		# Notification YouTube system
		response = self.requests_youtube()
		for id in self.id_all_videos:
			if id == response["items"][0]["contentDetails"]["upload"]["videoId"]:
				break
			await self.send_video_notification(response)
			self.id_all_videos.append(response["items"][0]["contentDetails"]["upload"]["videoId"])

	async def live_twitch_notification_system(self):
		s = self.request_twitch()
		try:
			if s['data'][0]['type'] == 'live':
				for n,stream_id in enumerate(self.all_streams):
					if int(s['data'][0]['id']) == int(stream_id):
						break
					if n == len(self.all_streams) - 1:
						await self.send_twitch_notification(s)
						self.all_streams.append(int(s['data'][0]['id']))
		except (KeyError,IndexError):
			pass

	def append_videos_ids(self):
		r = self.requests_youtube(max_r=9999999)
		for item in r["items"]:
			self.id_all_videos.append(item["contentDetails"]["upload"]["videoId"])

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
				b_role[role.name] = role;
				number_keys_b_role += 1
			for role in a.roles:
				a_role[role.name] = role;
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
					i = compare_role[role]
				except KeyError:
					role_update = role
			del i

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
		self.append_videos_ids()
		await self.api_event.start()

	@loop(minutes=1)
	async def api_event(self):
		await self.bot.wait_until_ready()
		await self.video_youtube_notification_system()
		await self.live_twitch_notification_system()
