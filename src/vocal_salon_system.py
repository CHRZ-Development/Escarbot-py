import datetime

from discord import utils
from discord.ext import commands


class VocalSalonSystem(commands.Cog):
    """ VocalSalonSystem() -> Represent the creation of vocal custom with anyone ! """

    def __init__(self,bot):
        self.bot = bot

    async def create_vocal(self,database,guild,member):
        """ create_vocal() -> Create a channel when the member as joined "Crée un salon" """
        category = utils.get(guild.categories,id=int(database["category_id"]))
        # Create and get the new vocal channel
        new_channel = await guild.create_voice_channel(f"{member.name}'s Channel.",bitrate=64000,category=category)
        # Log
        print(f"[{datetime.datetime.today().date()}] L'utilisateur {member.name} à crée un salon dans {guild.name} !")
        # Move the member to the vocal channel created
        await new_channel.edit(position=len(category.voice_channels)+1)
        await member.move_to(new_channel)

    async def delete_vocal(self,before,member):
        """ delete_vocal() -> Delete a channel when the member as leave your channel """
        # If 0 as in channel
        if before.channel is not None:
            if len(before.channel.members) == 0:
                # Log
                print(f"[{datetime.datetime.today().date()}] Le salon de {member.name} à été supprimé dans {member.guild.name} !")
                return await before.channel.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        for database in self.bot.guilds_data[str(member.guild.id)]["channels"]:
            if database["function"].count("create_private_vocal") == 1:
                if after.channel is not None:
                    if int(after.channel.id) == int(database["channel_id"]):
                        return await self.create_vocal(database,member.guild,member)
                if after.channel is None:
                    if int(before.channel.id) != int(database["channel_id"]):
                        return await self.delete_vocal(before,member)
