import os
import httplib2
import google_auth_oauthlib.flow
import googleapiclient.discovery

from typing import Any
from discord import Colour,Embed,utils


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
        except httplib2.error.ServerNotFoundError:
            pass
        else:
            return response

    async def video_notification_system(self):
        # Notification YouTube system
        response = self.requests()

        for _id in self.id_all_videos:
            if _id == response["items"][0]["contentDetails"]["upload"]["videoId"]:
                break
            await self.send_notification(response)
            self.id_all_videos.append(response["items"][0]["contentDetails"]["upload"]["videoId"])

    async def send_notification(self,r):
        for guild in self.bot.guilds:
            try:
                self.bot.guilds_data[str(guild.id)]["channels_ID"]["video_notif"]
            except KeyError:
                pass
            else:
                videos_role = utils.get(guild.roles,id=self.bot.guilds_data[str(guild.id)]["roles"]["🎬"])
                channel_videos = self.bot.get_channel(self.bot.guilds_data[str(guild.id)]["channels_ID"]["video_notif"])
                self.last_video = r["items"][0]["snippet"]["title"]
                video_message = Embed(title="> Un nouveau `🔴 Live`",colour=Colour.from_rgb(255,0,0))
                video_message.add_field(name=f"{r['items'][0]['snippet']['channelTitle']} vien de sortir une vidéo !",value=f"{videos_role.mention}\nhttps://youtu.be/{r['items'][0]['contentDetails']['upload']['videoId']}")
                video_message.set_author(name=guild.owner.name,icon_url=guild.owner.avatar_url)
                await channel_videos.send(embed=video_message)
