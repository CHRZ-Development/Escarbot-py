from discord import utils
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
            return stream
        except (TwitchAPIException,TwitchBackendException):
            pass

    async def send_notification(self,s):
        chrz_development = utils.get(self.bot.guilds,id=838862631284506705)
        live_role = utils.get(chrz_development.roles,id=self.bot.ids[chrz_development.id]['id_role_notify_live'])

        channel_live = self.bot.get_channel(self.bot.ids[chrz_development.id]['id_channel_live'])
        await channel_live.send(content=f'{live_role.mention}\n>  **Tien Tien Tien, {s["data"][0]["user_name"]} stream** "{s["data"][0]["title"]}" **actuellement !**\n https://www.twitch.tv/naulan_chrzdev ')

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
