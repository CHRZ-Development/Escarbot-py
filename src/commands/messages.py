import os

from discord import Colour,Embed
from discord.ext import commands


class MessagesCommand(commands.Cog):
    """ MessagesCommand() -> Represent the preset messages. """
    def __init__(self,bot):
        self.bot = bot
        self.send_message_func = {"custom_message": self.custom_message,"roles_message": self.roles_message}
        self.refresh_database = lambda: self.bot.file.write(self.bot.guilds_data,"guilds_data.json",f"{os.getcwd()}/res/")

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

    def rules_message(self):
        pass

    async def custom_message(self,ctx,messages):
        await ctx.send(content=messages[0])

    @commands.command(name="send")
    @commands.is_owner()
    async def send_message(self,ctx,option,*args):
        await self.send_message_func[option](ctx,args)
        await ctx.message.delete()

