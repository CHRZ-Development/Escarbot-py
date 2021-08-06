from discord import Colour,Embed,utils
from twitchAPI import Twitch,TwitchAPIException,TwitchBackendException


class TwitchAPI(object):
    twitch: Twitch
    all_streams: list = [00000000000]

    def __init__(self,bot):
        self.bot = bot
        self.app_id = self.bot.config["TWITCH"]["app_id"]
        self.app_secret = self.bot.config["TWITCH"]["app_secret"]

    def create(self):
        # create instance of twitch API
        self.twitch = Twitch(self.app_id,self.app_secret)
        self.twitch.authenticate_app([])
        # get ID of user
        user_info = self.twitch.get_users(logins=['NaulaN_CHRZdev'])
        self.user_id = user_info['data'][0]['id']

    def request(self):
        """ request_twitch( ) -> Send a request to twitch for will get a new live """
        # Check if stream
        try:
            stream = self.twitch.get_streams(user_id=self.user_id,first=1)
        except (TwitchAPIException,TwitchBackendException):
            pass
        else:
            return stream

    async def send_notification(self,s):
        for guild in self.bot.guilds:
            try:
                self.bot.guilds_data[str(guild.id)]["channels_ID"]["live_notif"]
            except KeyError:
                pass
            else:
                live_role = utils.get(guild.roles,id=self.bot.guilds_data[str(guild.id)]["roles"]["🔴"])
                channel_live = self.bot.get_channel(self.bot.guilds_data[str(guild.id)]["channels_ID"]["live_notif"])
                live_message = Embed(title="> Un nouveau `🔴 Live`",colour=Colour.from_rgb(127,0,255))
                live_message.add_field(name=f"{s['data'][0]['user_name']} est en live ! Vien vite il stream {s['data'][0]['title']} !",value=f"{live_role.mention}\nhttps://www.twitch.tv/naulan_chrzdev")
                live_message.set_author(name=guild.owner.name,icon_url=guild.owner.avatar_url)
                return await channel_live.send(embed=live_message)

    async def live_notification_system(self):
        s = self.request()
        try:
            if s['data'][0]['type'] == 'live':
                for n,stream_id in enumerate(self.all_streams):
                    if int(s['data'][0]['id']) == int(stream_id):
                        break
                    if n == len(self.all_streams) - 1:
                        await self.send_notification(s)
                        self.all_streams.append(int(s['data'][0]['id']))
        except (KeyError,IndexError):
            pass
