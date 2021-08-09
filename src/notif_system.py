from discord.ext import commands
from discord.ext.tasks import loop
from src.APIs.twitch import TwitchAPI
from src.APIs.youtube import YouTubeAPI


class NotificationSystem(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

		self.youtube_api = YouTubeAPI(self.bot)
		self.youtube_api.create()
		self.twitch_api = TwitchAPI(self.bot)
		self.twitch_api.create()

	@commands.Cog.listener()
	async def on_ready(self):
		self.youtube_api.append_videos_ids()
		await self.api_event.start()

	@loop(minutes=1)
	async def api_event(self):
		await self.bot.wait_until_ready()
		await self.youtube_api.video_notification_system()
		await self.twitch_api.live_notification_system()
