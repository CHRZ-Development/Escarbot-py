import os

from discord import Colour,Embed
from discord.ext import commands


class MessagesCommand(commands.Cog):
    """ MessagesCommand() -> Represent the preset messages. """
    def __init__(self,bot):
        self.bot = bot
        self.send_message_func = {"custom_message": self.custom_message,"roles_message": self.roles_message,"embed_message": self.embed_message}
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

    async def embed_message(self,ctx,messages):
        opt1,*tle = messages[0].split("=")
        opt2,*color = messages[1].split("=")
        if opt1 == "title":
            if opt2 in ["colour", "color"]:
                r,g,b = str(color[0]).split(",")
                custom_message = Embed(title="".join(tle),colour=Colour.from_rgb(int(r),int(g),int(b)))
            else:
                custom_message = Embed(title="".join(tle))
        else:
            custom_message = Embed()
        titles = [];details = []
        for n,title in enumerate(messages):
            if int(n) in [2,4,6,8,10,12,14,16,18,20]:
                titles.append(title)
            else:
                if int(n) >= 2:
                    details.append(title)
        for n,part in enumerate(titles):
            custom_message.add_field(name=titles[n],value=details[n])
        await ctx.send(embed=custom_message)

    @commands.command(name="send")
    @commands.is_owner()
    async def send_message(self,ctx,option,*args):
        await self.send_message_func[option](ctx,args)
        await ctx.message.delete()

