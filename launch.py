#!/bin/python3.8
from discord_components import DiscordComponents

from bot import Bot

escarbot = Bot()
DiscordComponents(escarbot)
escarbot.run(escarbot.config["BOT"]["TOKEN"])
