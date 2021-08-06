import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import httplib2

from typing import Any
from discord import utils


class YouTubeAPI(object):
    youtube: Any
    id_all_videos: list = []

    def __init__(self,bot):
        self.bot = bot
        self.__client_secrets_file = self.bot.config["YOUTUBE"]["client_secrets_file"]
        self.__api_service_name = self.bot.config["YOUTUBE"]["api_service_name"]
        self.__api_version = self.bot.config["YOUTUBE"]["api_version"]
        self.__scopes = [self.bot.config["YOUTUBE"]["scopes"]]
        self.__channel_id = self.bot.config["YOUTUBE"]["channel_id"]

    def append_videos_ids(self):
        r = self.requests(max_r=9999999)
        for item in r["items"]:
            self.id_all_videos.append(item["contentDetails"]["upload"]["videoId"])

    def create(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.__client_secrets_file,self.__scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(self.__api_service_name,self.__api_version,credentials=credentials)

    def requests(self,max_r=1,p="snippet,contentDetails,id"):
        """ request_youtube( ) -> Send a request to youtube for will get a new videos. """
        request = self.youtube.activities().list(part=p,channelId=self.__channel_id,maxResults=max_r)

        try:
            response = request.execute()
            return response
        except httplib2.error.ServerNotFoundError:
            pass

    async def video_notification_system(self):
        # Notification YouTube system
        response = self.requests()

        for _id in self.id_all_videos:
            if _id == response["items"][0]["contentDetails"]["upload"]["videoId"]:
                break
            await self.send_notification(response)
            self.id_all_videos.append(response["items"][0]["contentDetails"]["upload"]["videoId"])

    async def send_notification(self,r):
        chrz_development = utils.get(self.bot.guilds,id=838862631284506705)
        videos_role = utils.get(chrz_development.roles,id=self.bot.ids[chrz_development.id]['id_role_notify_videos'])

        channel_videos = self.bot.get_channel(self.bot.ids[chrz_development.id]['id_channel_videos'])
        self.last_video = r["items"][0]["snippet"]["title"]
        await channel_videos.send(content=f'{videos_role.mention}\n>  **Oh ! __{r["items"][0]["snippet"]["channelTitle"]}__ à publié une __nouvelle vidéo__ !** \n👍 + 💬 + 🔔 = ✅ Merciii !\nhttps://youtu.be/{r["items"][0]["contentDetails"]["upload"]["videoId"]}')
