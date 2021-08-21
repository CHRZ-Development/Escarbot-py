import datetime
import os

from discord import DMChannel,Embed,Forbidden,PermissionOverwrite,TextChannel,utils
from discord.ext import commands
from discord_slash import ButtonStyle,ComponentContext
from discord_slash.utils.manage_components import create_button,create_actionrow


class TicketSystem(commands.Cog):
    def __init__(self,bot):
        self.refresh_database = lambda file: self.bot.file.write(self.bot.guilds_data if file == "guilds_data.json" else self.bot.users_data,file,f"{os.getcwd()}/res/")
        self.id_ticket_open = {}
        with open(os.path.join(f"{os.getcwd()}/res/","all_tickets_number.txt")) as f:
            self.id_ticket = int(f.read())
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.id_ticket_open[str(guild.id)] = []

    @commands.Cog.listener()
    async def on_component(self,ctx: ComponentContext):
        # If a user
        if str(ctx.custom_id) == "Ticket":
            self.id_ticket += 1
            ticket_msg = Embed(title="> ✉ Vous avez ouvert un ticket.",description=f"Guild={ctx.guild_id}\nID Ticket={self.id_ticket}")
            ticket_msg.add_field(name="Confirmez votre ticket !",value="Appuyez sur le bouton `✅ Je confirme.` pour confirmer votre ✉ ticket !")
            ticket_msg.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
            ticket_msg.set_footer(text="Votre serviteur, Escarbot vous fera le lien avec un membre du staff.",icon_url=self.bot.user.avatar_url)
            ticket_button = create_button(style=ButtonStyle.green,label="Je confirme.",emoji="✅",custom_id="Ticket_confirmed")
            ticket_action_row = create_actionrow(ticket_button)
            try:
                message = await ctx.author.send(embed=ticket_msg,components=[ticket_action_row])
                msg = "📤 Un message vous a été envoyé !"
            except Forbidden:
                msg = "⚙ Activer le parametre `Autoriser les messages privés venant des membres du serveur`"
            else:
                try:
                    self.bot.users_data[str(ctx.guild.id)][str(ctx.author.id)]["tickets"][str(message.channel.id)]["enabled"] = True
                except KeyError:
                    self.bot.users_data[str(ctx.guild.id)][str(ctx.author.id)]["tickets"] = {str(message.channel.id): {"enabled": True,"confirmed": False,"id": 0,"closed": False}}
            self.refresh_database("users_data.json")
            with open(os.path.join(f"{os.getcwd()}/res/","all_tickets_number.txt"),"w") as f:
                f.write(str(self.id_ticket))
            return await ctx.send(content=msg,hidden=True)

        if ctx.custom_id == "Ticket_confirmed":
            # Get ticket id and guild id
            guild_info,ticket_info = str(ctx.origin_message.embeds[0].description).split("\n")
            guild_param,guild_id = guild_info.split("=")
            ticket_param,ticket_id = ticket_info.split("=")
            guild = utils.get(self.bot.guilds,id=int(guild_id))
            # Update database
            self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.origin_message.channel.id)]["id"] = int(ticket_id)
            self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"]["message_id"] = int(ctx.origin_message.id)
            await ctx.origin_message.edit(components=None)
            if self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["enabled"]:
                category = None
                for catgory in guild.categories:
                    if str(catgory.name) == "✉ Tickets":
                        category = catgory
                        break
                if category is None:
                    def set_permissions(bool_: bool):
                        perms = PermissionOverwrite()
                        perms.view_channel = bool_
                        return perms
                    category = await guild.create_category(name="✉ Tickets",position=len(guild.categories))
                    await category.set_permissions(guild.roles[0],overwrite=set_permissions(False))
                confirmed_ticket_msg = Embed()
                confirmed_ticket_msg.set_author(name=guild.name,icon_url=guild.icon_url)
                confirmed_ticket_msg.add_field(name="Votre demande à était prise en compte !",value="Attendez que quelqu'un vous répond !")
                text_channel = await guild.create_text_channel(name=f"{ctx.author.id} Ticket",category=category)
                self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["text_channel"] = text_channel.id
                self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["confirmed"] = True
                self.refresh_database("users_data.json")
                return await ctx.author.send(embed=confirmed_ticket_msg)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot is False:
            for guild in self.bot.guilds:
                # If in private message channel
                if isinstance(message.channel,DMChannel):
                    try:
                        msg_info = await message.channel.fetch_message(id=self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"]["message_id"])
                        # text_channel = guild.get_channel(self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["text_channel"])
                    except KeyError:
                        pass
                    else:
                        guild_info,ticket_info = str(msg_info.embeds[0].description).split("\n")
                        ticket_param,ticket_id = ticket_info.split("=")
                        if int(self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["id"]) == int(ticket_id):
                            if self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["confirmed"]:
                                text_channel = guild.get_channel(self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["text_channel"])
                                if text_channel is not None:
                                    msg = Embed()
                                    msg.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                                    msg.add_field(name=f"Envoyé le {datetime.datetime.today().date()} à {datetime.datetime.today().time()}",value=message.content)
                                    return await text_channel.send(embed=msg)
                # If in text channel
                if isinstance(message.channel,TextChannel):
                    if str(message.channel.category.name) == "✉ Tickets":
                        id_,*name_channel = str(message.channel.name).split("-")
                        member = utils.get(message.guild.members,id=int(id_))
                        return await member.send(content=message.content)
