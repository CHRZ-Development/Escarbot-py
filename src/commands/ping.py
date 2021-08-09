from discord import Colour,Embed
from discord.ext import commands


class PingCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.get_latency = lambda: round(self.bot.latency*1000)

    @staticmethod
    def ping_indicator(latency):
        if latency <= 100.0:
            indicator = "🟢"
        elif 100.0 <= latency <= 200.0:
            indicator = "🟠"
        elif latency >= 200.0:
            indicator = "🔴"
        return indicator

    @commands.command(name="ping")
    async def ping_request(self,ctx):
        bot_latency = self.get_latency()
        indicator = self.ping_indicator(bot_latency)
        ping_message = Embed(colour=Colour.from_rgb(96,96,96))
        ping_message.add_field(name="> **Ping Request.**",value=f"{indicator} latency: **{bot_latency}** ms")
        ping_message.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        ping_message.set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=ping_message)
