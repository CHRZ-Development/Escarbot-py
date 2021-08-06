import os
import json

from discord import Colour,Embed
from discord.ext import commands


class MessagesCommand(commands.Cog):
    """ MessagesCommand() -> Represent the preset messages. """
    def __init__(self,bot):
        self.bot = bot
        self.send_message_func = {"custom_message": self.custom_message,
                                  "roles_message": self.roles_message}

    async def roles_message(self,ctx,colour):
        """ roles_message() -> It allow to attribute a role thanks to reactions below a message. """
        guild_id = str(ctx.guild.id)
        r,g,b = colour
        # Title.
        roles_info_available = "\n**Les rôles disponibles sont:**\n"
        # Get roles available.
        roles_list_available = []
        for role in self.bot.guilds_data[guild_id]["roles_can_attributes"]:
            roles_list_available.append(f"_ _`{self.bot.guilds_data[guild_id]['roles_emoji_reaction'][role]}` **|** {self.bot.guilds_data[guild_id]['roles_info'][role]}\n")
        roles_available = ' '.join(roles_list_available)
        # Create Embed with a RGB color attribute.
        roles_message = Embed(colour=Colour.from_rgb(int(r),int(g),int(b)))
        # Add roles available message.
        roles_message.add_field(name="> 📌 Information et liste des rôles disponible sur ce serveur !\n",value=f"{roles_info_available}{roles_available}")
        # Send message and get this one.
        message = await ctx.send(embed=roles_message)
        self.bot.guilds_data[guild_id]["messages_ID"]["roles"] = int(message.id)
        # Add reactions on the message as been sending.
        for emoji in self.bot.guilds_data[guild_id]['roles_emoji_reaction']:
            await message.add_reaction(self.bot.guilds_data[guild_id]['roles_emoji_reaction'][emoji])
        self.refresh_database()

    def welcome_message(self):
        pass

    def rules_message(self):
        pass

    def level_up_message(self):
        pass

    def live_message(self):
        pass

    def video_message(self):
        pass

    def announcements_message(self):
        pass

    def ban_message(self):
        pass

    def mute_message(self):
        pass

    def join_message(self):
        pass

    def nitro_booster_message(self):
        pass

    async def custom_message(self,ctx,messages):
        await ctx.send(content=messages[0])

    def refresh_database(self):
        with open(os.path.join(f"{os.getcwd()}/res/","guilds_data.json"),"w") as f:
            json.dump(self.bot.guilds_data,f)

    @commands.command(name="send")
    @commands.is_owner()
    async def send_message(self,ctx,option,*args):
        await self.send_message_func[option](ctx,args)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,event):
        pass

