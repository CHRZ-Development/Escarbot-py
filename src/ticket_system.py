import datetime
import os

from discord import DMChannel,Embed,Forbidden,Message,PermissionOverwrite,TextChannel,utils
from discord.ext import commands
from discord_slash import ButtonStyle,ComponentContext
from discord_slash.utils.manage_components import create_button,create_actionrow


class TicketSystem(commands.Cog):
    """ TicketSystem() -> Represent a ticket system. """
    def __init__(self,bot):
        # Get number of ticket sending for id
        with open(os.path.join(f"{os.getcwd()}/res/","all_tickets_number.txt")) as f:
            self.id_ticket = int(f.read())
        self.bot = bot

    async def dm_channel_to_text_channel(self,message: Message) -> Message:
        """ dm_channel_to_text_channel() -> Transfers a message from a DM channel to text channel in a guild.
                :return: sending a message in a text channel (defined in open_ticket()) in the ✉ Tickets category. """
        if isinstance(message.channel,DMChannel):
            for guild in self.bot.guilds:
                try:
                    msg_info = await message.channel.fetch_message(id=self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"]["message_id"])
                except KeyError:
                    pass
                else:
                    # Get ticket id
                    guild_info,ticket_info = str(msg_info.embeds[0].description).split("\n")
                    ticket_param,ticket_id = ticket_info.split("=")
                    if int(self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["id"]) == int(ticket_id):
                        if self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["confirmed"]:
                            text_channel = guild.get_channel(self.bot.users_data[str(guild.id)][str(message.author.id)]["tickets"][str(message.channel.id)]["text_channel"])
                            # Send message dm channel to text channel
                            if text_channel is not None:
                                msg = Embed()
                                msg.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                                msg.add_field(name=f"Envoyé le {datetime.datetime.today().date()} à {datetime.datetime.today().time()}",value=message.content)
                                return await text_channel.send(embed=msg)

    async def text_channel_to_dm_channel(self,message: Message) -> Message:
        """ text_channel_to_dm_channel() -> Transfers a message from a text channel in a guild to DM channel.
                :return: sending a message to member who have open ticket thanks to the name of text channel in a guild. """
        if isinstance(message.channel,TextChannel):
            if str(message.channel.category.name) == "✉ Tickets":
                # Get member id thanks to the name of Text Channel
                id_,*name_channel = str(message.channel.name).split("-")
                member = utils.get(message.guild.members,id=int(id_))
                # Send DM
                return await member.send(content=message.content)

    async def open_ticket(self,ctx: ComponentContext) -> Message:
        """ open_ticket() -> Send a confirmation message for open a ticket. """
        print(f"[{datetime.datetime.today().date()}] L'utilisateur {ctx.author.name} à commence a ouvrir un ticket.")
        # Refresh ID Tickets
        self.id_ticket += 1
        # Message of confirmation
        ticket_msg = Embed(title="> ✉ Vous avez ouvert un ticket.",description=f"Guild={ctx.guild_id}\nID Ticket={self.id_ticket}")
        ticket_msg.add_field(name="Confirmez votre ticket !",value="Appuyez sur le bouton `✅ Je confirme.` pour confirmer votre ✉ ticket !")
        ticket_msg.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
        ticket_msg.set_footer(text="Votre serviteur, Escarbot vous fera le lien avec un membre du staff.",icon_url=self.bot.user.avatar_url)
        # Create a button and a action
        ticket_button = create_button(style=ButtonStyle.green,label="Je confirme.",emoji="✅",custom_id="Ticket_confirmed")
        ticket_action_row = create_actionrow(ticket_button)
        try:
            # Can send the message, send a information
            message = await ctx.author.send(embed=ticket_msg,components=[ticket_action_row])
            msg = "📤 Un message vous a été envoyé !"
        except Forbidden:
            # Can't sending the message, send a tips
            msg = "⚙ Activer le parametre `Autoriser les messages privés venant des membres du serveur`"
        else:
            try:
                self.bot.users_data[str(ctx.guild.id)][str(ctx.author.id)]["tickets"][str(message.channel.id)]["enabled"] = True
            except KeyError:
                self.bot.users_data[str(ctx.guild.id)][str(ctx.author.id)]["tickets"] = {str(message.channel.id): {"enabled": True,"confirmed": False,"id": 0,"closed": False}}
        self.bot.refresh_database("users_data.json")
        with open(os.path.join(f"{os.getcwd()}/res/","all_tickets_number.txt"),"w") as f:
            f.write(str(self.id_ticket))
        return await ctx.send(content=msg,hidden=True)

    async def confirmed_ticket_opened(self,ctx: ComponentContext) -> Message:
        """ confirmed_ticket_opened() -> Confirm the ticket after a interaction on the Ticket_confirmed button. """
        # Get ticket id and guild id
        guild_info,ticket_info = str(ctx.origin_message.embeds[0].description).split("\n")
        guild_param,guild_id = guild_info.split("=")
        ticket_param,ticket_id = ticket_info.split("=")
        guild = utils.get(self.bot.guilds,id=int(guild_id))
        # Update database
        self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.origin_message.channel.id)]["id"] = int(ticket_id)
        self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"]["message_id"] = int(ctx.origin_message.id)
        # Delete the button
        await ctx.origin_message.edit(components=None)
        # If a ticket is active
        if self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["enabled"]:
            category = None
            # Search if the category is already exist
            for catgory in guild.categories:
                if str(catgory.name) == "✉ Tickets":
                    category = catgory
                    break
            # If not exist ✉ Tickets category, create the category
            if category is None:
                def set_permissions(bool_: bool):
                    perms = PermissionOverwrite()
                    perms.view_channel = bool_
                    return perms
                category = await guild.create_category(name="✉ Tickets",position=len(guild.categories))
                # Owner can view the category
                await category.set_permissions(guild.roles[0],overwrite=set_permissions(False))
            # Message confirmed ticket
            confirmed_ticket_msg = Embed()
            confirmed_ticket_msg.set_author(name=guild.name,icon_url=guild.icon_url)
            confirmed_ticket_msg.add_field(name="Votre demande à était prise en compte !",value="Attendez que quelqu'un vous répond !")
            # Search if a text channel is already exist
            text_channel = utils.get(guild.channels,name=f"{ctx.author.id}-ticket")
            # If not exist text channel, create a text channel
            if text_channel is None:
                text_channel = await guild.create_text_channel(name=f"{ctx.author.id}-ticket",category=category)
            # Update database
            self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["text_channel"] = text_channel.id
            self.bot.users_data[str(guild.id)][str(ctx.author.id)]["tickets"][str(ctx.channel.id)]["confirmed"] = True
            self.bot.refresh_database("users_data.json")
            return await ctx.author.send(embed=confirmed_ticket_msg)

    @commands.Cog.listener()
    async def on_component(self,ctx: ComponentContext):
        # If a user at click the button
        if str(ctx.custom_id) == "Ticket":
            await self.open_ticket(ctx)
        # If a user at click the button in dm
        if ctx.custom_id == "Ticket_confirmed":
            await self.confirmed_ticket_opened(ctx)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot is False:
            await self.text_channel_to_dm_channel(message)
            await self.dm_channel_to_text_channel(message)
