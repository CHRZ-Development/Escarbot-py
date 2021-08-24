# -*- coding: UTF-8 -*-
""" =======================================================================

     ██████   █████                      ████            ██████   █████
    ░░██████ ░░███                      ░░███           ░░██████ ░░███
     ░███░███ ░███   ██████   █████ ████ ░███   ██████   ░███░███ ░███
     ░███░░███░███  ░░░░░███ ░░███ ░███  ░███  ░░░░░███  ░███░░███░███
     ░███ ░░██████   ███████  ░███ ░███  ░███   ███████  ░███ ░░██████
     ░███  ░░█████  ███░░███  ░███ ░███  ░███  ███░░███  ░███  ░░█████
     █████  ░░█████░░████████ ░░████████ █████░░████████ █████  ░░█████
    ░░░░░    ░░░░░  ░░░░░░░░   ░░░░░░░░ ░░░░░  ░░░░░░░░ ░░░░░    ░░░░░

===========================================================================
◻ Doc discord.py: https://discordpy.readthedocs.io/en/stable/api.html
◻ Dev Discord Guild: https://discord.gg/yEvBg8CPaM
◻ YouTube Channel: https://www.youtube.com/channel/UCbl4AHVket_DNhBzQG56f7w
======================================================================= """
import os
import json
import datetime

from googletrans import Translator
from discord import Colour,Embed,Intents,Message
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord_slash import ButtonStyle,ComponentContext,SlashCommand,SlashContext
from discord_slash.utils.manage_components import create_actionrow,create_button,wait_for_component

from commands.get import GetCommand
from src.commands.mute import MuteCommand
from src.commands.ban import BanCommand
from src.commands.help import HelpCommand
from src.commands.edit import EditCommand
from src.commands.ping import (PingCommand,PingSlash)
from src.commands.unban import UnBanCommand
from src.commands.nickname import (Nickname,NicknameCommand,NicknameSlash)
from src.commands.myvocal import (MyVocalCommand,MyVocalSlash)
from src.commands.userinfo import (UserInfoCommand,UserInfoSlash)
from src.commands.messages import (MessagesCommand,MessagesSlash)
from src.commands.serverinfo import (ServerInfoCommand,ServerInfoSlash)
from src.commands.attributes import AttributesCommand
from src.activities import Activities
from src.roles_sytem import RolesSystem
from src.file_manager import FileManager
from src.analytics_system import Analytics
from src.backup_system import BackupSystem
from src.database_system import DataBaseSystem
from src.notif_system import NotificationSystem
from src.vocal_salon_system import VocalSalonSystem
from src.auto_messages_send_system import AutoMessagesSendSystem
from src.ticket_system import TicketSystem


def set_permissions() -> Intents:
    """ set_permission() -> All permission for the Bot."""
    perms = Intents.all()
    perms.bans = True
    perms.guilds = True
    perms.members = True
    perms.messages = True
    perms.reactions = True
    perms.presences = True
    perms.voice_states = True
    perms.guild_messages = True
    perms.guild_reactions = True
    return perms


class Bot(commands.Bot):
    """ Bot() -> Represent a Bot discord """
    def __init__(self):
        commands.Bot.__init__(self,intents=set_permissions(),command_prefix="!",help_command=None)
        self.slash = SlashCommand(client=self,sync_commands=True)
        self.file = FileManager()
        self.translator = Translator()
        self.config = self.file.load("cfg.ini",f"{os.getcwd()}/res/")
        # Messages
        self.titles = ["> ❌ | Erreur !","> ✅ | Effectué !"]
        self.success_footer = ["Effectué avec succès grâce à Escarbot, votre serviteur !","Utilisé les nouvelles commandes slash ! Effectué avec succès grâce à Escarbot, votre serviteur !"]
        self.error_footer = ["Escarbot n'a pas pu effectué votre demande !","Utilisé les nouvelles commandes slash ! Escarbot n'a pas pu effectué votre demande !"]
        # Template for database
        self.template = {"roles_can_attributes": [],"roles_emoji_reaction": {},"functions": {"stat": False,"verif_rules": True,"create_personal_vocal": False},"categories_ID": {"vocals_channel": 0},"vocals_ID": {"create_vocal": 0},"messages_ID": {"roles": 0,"rules": 0,"stat": 0,},"messages": {"welcome": [],"rules": {"authorized": [],"forbidden": [],"verif_rules": ["> Avez-vous pris connaisance des régles ?","Si oui, clické sur la reaction ci-dessous"]}},"roles": {},"roles_info": {}}
        self.template_user = {"JoinedAt": {"Year": 0,"Month": 0,"Day": 0},"CriminalRecord": {"NumberOfMutes": 0,"NumberOfWarnings": 0,"NumberOfReports": 0,"NumberOfBans": 0,"BanInfo": {"Definitive": False,"IsBanned": False,"WhoAtBanned": None,"WhenHeAtBeenBanned": {"Year": None,"Month": None,"Day": None},"TimeOfBan": {"Year": None,"Month": None,"Day": None}},"MuteInfo": {"IsMuted": False,"WhoAtMute": None,"WhenHeAtBeenBanned": {"Year": None,"Month": None,"Day": None,"Hour": None},"TimeOfMute": {"Year": None,"Month": None,"Day": None,"Hours": None}},"BanSystem": {"day_counter": 0,"how_much_days": 0},"MuteSystem": {},"ReportInfo": {"NumberOfReports": 0,"WhoReportedIt": {"Users": [],"When": [],"Messages": []}},"RestrictedInfo": {"IsRestricted": False,"WhoAtRestricted": None,"WhenHeAtBeenRestricted": {"Year": None,"Month": None,"Day": None,"Hour": None},"TimeOfRestricted": {"Year": None,"Month": None,"Day": None}}},"NumberOfMessages": {}}
        # Guilds settings
        guilds_data_path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
        with open(guilds_data_path) as f:
            self.guilds_data = json.load(f)
        # User database per guilds
        user_info_path = os.path.join(f"{os.getcwd()}/res/","users_data.json")
        with open(user_info_path) as f:
            self.users_data = json.load(f)
        self.refresh_database = lambda file: self.file.write(self.guilds_data if file == "guilds_data.json" else self.users_data,file,f"{os.getcwd()}/res/")
        # Add all commands and systems
        self.add_all_cogs()

    async def check_permission(*args):
        self,ctx = args
        for n,role_database in enumerate(self.guilds_data[str(ctx.guild.id)]["roles"]):
            for role in ctx.author.roles:
                if (int(role_database["role_id"]) == int(role.id)) and (role_database["can_execute_command"].count(ctx.command.name) >= 1):
                    return True
            if int(n) == len(self.guilds_data[str(ctx.guild.id)]["roles"])-1:
                return False

    async def send_message_after_invoke(self,ctx,success_msg: list,error_msg: list,action=None,value=None,_error=None):
        msg = Embed(title=self.titles[0] if value is None else self.titles[1])
        # Send successfully message embed
        if value is not None:
            msg.add_field(name=success_msg[0],value=success_msg[1](value))
            msg.set_footer(text=self.success_footer[0],icon_url=self.user.avatar_url) if isinstance(ctx,SlashContext) or isinstance(ctx,Message) else msg.set_footer(text=self.success_footer[1],icon_url=self.user.avatar_url)
        # Send error message embed
        if _error is not None:
            msg.add_field(name=error_msg[0][0],value=error_msg[0][1](_error)) if len(error_msg) == 1 else msg.add_field(name=error_msg[1][0],value=error_msg[1][1],inline=False)
            msg.set_footer(text=self.error_footer[0],icon_url=self.user.avatar_url) if isinstance(ctx,SlashContext) or isinstance(ctx,Message) else msg.set_footer(text=self.error_footer[1],icon_url=self.user.avatar_url)
        msg.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        return await ctx.channel.send(embed=msg) if isinstance(ctx,Message) else await ctx.send(embed=msg,components=action)

    async def can_rename_after_invoke_command(self,cog,ctx,action):
        create_msg = lambda name,value,author: Embed().add_field(name=name,value=value).set_author(name=author.name,icon_url=author.avatar_url)
        # Wait pressed "🤭 Une faute ?" Buttton
        wrong_button_interaction: ComponentContext = await wait_for_component(self,components=action,timeout=60)
        cancel_button = create_actionrow(create_button(style=ButtonStyle.red,label="Tu ne veux plus le changé ?",emoji="🧐"))
        # On pressed "🤭 Une faute ?" Button, send message
        if wrong_button_interaction.author != ctx.author:
            return await wrong_button_interaction.send(embed=create_msg("⚠ Utilisateur non autorisé","Vous n'etes pas autorisé d'appuie sur ce bouton !",wrong_button_interaction.author))
        await wrong_button_interaction.send(embed=create_msg("Vous avez appuyé sur le bouton `Une faute ?`.","Entrez votre nouveau pseudo ou nom de vocal !",ctx.author),components=[cancel_button])
        # Wait pressed "🧐 Tu ne veux plus le changé ?" Button
        cog.data[str(ctx.author.id)] = [True,True]
        cancel_button_interaction: ComponentContext = await wait_for_component(self,components=cancel_button,timeout=60)
        if cog.data[str(ctx.author.id)][1]:
            # On pressed "🧐 Tu ne veux plus le changé ?" Button, send message
            await cancel_button_interaction.send(embed=create_msg("Vous avez appuyé sur le bouton `Tu ne veux plus le changé ?`.",f"Vous avez fermez la possibilité de changé votre pseudo du a une faute de frappe ou bien d'un mauvais pseudo.\nVous pouvez toujours executé la commande `/{ctx.command}` apres ca.",ctx.author).set_footer(text=self.success_footer[0],icon_url=self.user.avatar_url))
        cog.data.pop(str(ctx.author.id))

    def add_all_cogs(self):
        all_slashes = [NicknameSlash(self),MyVocalSlash(self),PingSlash(self),ServerInfoSlash(self),UserInfoSlash(self),MessagesSlash(self)]
        self.add_cog(all_slashes[0])
        self.add_cog(all_slashes[1])
        for slash in all_slashes:
            self.slash.get_cog_commands(slash)
        all_commands = [GetCommand(self),MuteCommand(self),NicknameCommand(self),ServerInfoCommand(self),UserInfoCommand(self),PingCommand(self),MyVocalCommand(self),UnBanCommand(self),BanCommand(self),EditCommand(self),MessagesCommand(self),AttributesCommand(self),HelpCommand(self)]
        for command in all_commands:
            self.add_cog(command)
        all_systems = [TicketSystem(self),DataBaseSystem(self),AutoMessagesSendSystem(self),BackupSystem(self),Analytics(self),RolesSystem(self),VocalSalonSystem(self)]
        for system in all_systems:
            self.add_cog(system)

    async def on_ready(self):
        await self.change_presence(activity=Activities(version=self.config["BOT"]["version"]))

    async def on_command_error(self,ctx,ex):
        print(ex,type(ex))
        if isinstance(ex,CommandNotFound):
            return await ctx.send(embed=Embed(description=self.translator.translate(src="en",dest="fr",text=str(ex)).text,colour=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
        error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda _error: self.translator.translate(src="en",dest="fr",text=str(_error)).text]]
        return await self.send_message_after_invoke(ctx,[],error_msg,_error=ex)

    async def on_slash_command_error(self,ctx,ex):
        print(ex,type(ex))
        if ctx.name == "nickname":
            error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda _error: self.translator.translate(src="en",dest="fr",text=str(_error)).text],["Votre pseudo doit contenir:","`" + "".join(Nickname.accept_letter) + "`"]]
            return await self.send_message_after_invoke(ctx,[],error_msg,_error=ex)
        error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda _error: self.translator.translate(src="en",dest="fr",text=str(_error)).text]]
        return await self.send_message_after_invoke(ctx,[],error_msg,_error=ex)
