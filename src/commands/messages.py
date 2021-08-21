import os

from discord import Colour,Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import ButtonStyle,SlashContext,cog_ext
from discord_slash.utils.manage_components import create_actionrow,create_button


class Messages(object):
    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
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

    async def rules_message(self,ctx,args):
        rules_msg = Embed(title="> 🧐 Avez-vous lu·e les règles ?",colour=Colour.from_rgb(0,255,0))
        rules_msg.add_field(name="Si oui 👇",value="Appuyez sur le bouton `🚪 Entrez dans le serveur !`")
        rules_msg.set_footer(text="❗ Lors de l'appui sur ce bouton, il vous permet d'accéder au serveur !")
        rules_buttons = [create_button(style=ButtonStyle.green,label="Entrez dans le serveur !",emoji="🚪",custom_id="Rules_accepted")]
        rules_action_row = create_actionrow(*rules_buttons)
        return await ctx.send(embed=rules_msg,components=[rules_action_row])

    async def ticket_message(self,ctx,args):
        ticket_msg = Embed(colour=Colour.from_rgb(128,128,128))
        ticket_msg.add_field(name="> Un problème ?",value="Appuyez sur le bouton `✉ Crée un ticket.`")
        ticket_msg.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
        ticket_msg.set_footer(text="❗ Lors de l'appui sur ce bouton, votre serviteur Escarbot vous mettra en lien avec un membre du staff apres une confirmation du ticket.")
        ticket_button = [create_button(style=ButtonStyle.grey,label="Crée un ticket.",emoji="✉",custom_id="Ticket")]
        ticket_action_row = create_actionrow(*ticket_button)
        return await ctx.send(embed=ticket_msg,components=[ticket_action_row])

    async def custom_message(self,ctx,messages):
        await ctx.send(content=messages[0])

    async def embed_message(self,ctx,messages):
        set_author = messages[0]
        opt1,*tle = messages[1].split("=")
        opt2,*color = messages[2].split("=")
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
            if int(n) in [3,5,7,9,11,13,15,17,19,21]:
                titles.append(title)
            else:
                if int(n) >= 3:
                    details.append(title)
        for n,part in enumerate(titles):
            custom_message.add_field(name=titles[n],value=details[n],inline=False)
        if set_author == "serveur":
            custom_message.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
        if set_author == "author":
            custom_message.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        await ctx.send(embed=custom_message)


class MessagesCommand(Messages,commands.Cog):
    """ MessagesCommand() -> Represent the preset messages. """
    def __init__(self,bot):
        Messages.__init__(self,self,bot)
        self.bot = bot
        self.send_message_func = {"custom_message": self.custom_message,"roles_message": self.roles_message,"embed_message": self.embed_message,"rules_message": self.rules_message,"ticket_message": self.ticket_message}

    @commands.command(name="send")
    @commands.is_owner()
    async def send_message(self,ctx,option,*args):
        await self.send_message_func[option](ctx,args)
        await ctx.message.delete()


class MessagesSlash(Messages,commands.Cog):
    def __init__(self,bot):
        Messages.__init__(self,self,bot)
        self.bot = bot
        self.send_rules.add_check(self.send_rules_check)

    @cog_ext.cog_subcommand(base="send",name="rules")
    async def send_rules(self,ctx: SlashContext):
        await self.rules_message(ctx,None)

    async def send_rules_check(*args): return True if int(args[1].guild.owner_id) == int(args[1].author.id) else False
