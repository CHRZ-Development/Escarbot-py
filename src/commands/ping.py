from discord import Colour,Embed
from discord.ext import commands
from discord_slash import SlashContext,cog_ext


class Ping(object):
    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
        self.get_latency = lambda: round(self.bot.latency*1000)
        self.obj.ping_request.add_check(self.bot.check_permission)

    def ping_indicator(self,latency) -> str:
        indicator = "🟢" if latency <= 100.0 else "🟠" if 100.0 <= latency <= 200.0 else "🔴"
        return indicator

    async def ping_message(self,ctx):
        bot_latency = self.get_latency()
        indicator = self.ping_indicator(bot_latency)
        ping_message = Embed(colour=Colour.from_rgb(96,96,96))
        ping_message.add_field(name="> **Ping Request.**",value=f"{indicator} latency: **{bot_latency}** ms")
        ping_message.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        ping_message.set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url)
        return await ctx.send(embed=ping_message)


class PingCommand(Ping,commands.Cog):
    def __init__(self,bot):
        Ping.__init__(self,self,bot)
        self.bot = bot

    @commands.command(name="ping")
    async def ping_request(self,ctx): return await self.ping_message(ctx)


class PingSlash(Ping,commands.Cog):
    def __init__(self,bot):
        Ping.__init__(self,self,bot)
        self.bot = bot

    @cog_ext.cog_slash(name="ping",description="Determine la latence (en ms) entre l'envoie et la reception d'un packet.")
    async def ping_request(self,ctx: SlashContext): return await self.ping_message(ctx)
