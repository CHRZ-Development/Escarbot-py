# -*- coding: UTF-8 -*-
from discord.ext import commands
from discord import Colour,Embed


class HelpCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.commands_info = {
            "attribute": [
                """
                :white_small_square: `!attribute role_emoji`
                :white_small_square: `!attribute role_info`
                :white_small_square: `!attribute role`
                :white_small_square: `!attribute channel`
                :white_small_square: `!attribute members_stat`
                :white_small_square: `!attribute rules_message`
                :white_small_square: `!attribute create_personal_vocal`
                :white_small_square: `!attribute perm_command`
                """,
                {
                    "channel": "Permet d'attribué des salons textuels",
                    "role_emoji": "Permet d'attribué un emoji à chaque rôle !\n__Exemple__: `!attribute role_emoji actuality_role 📰`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "role_info": "Permet de donné plus d'information sur un rôle !\n__Exemple__: `!attribute role_info member_role 'Le role par defaut'`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "role": "Permet d'attribué l'emoji a un rôle !\n__Exemple__: `!attribute role 📰 859421483524423690`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "members_stat": "Permet d'attribué un salon vocaux pour affiché le nombre de membres presentement dans le serveur Discord\n__Exemple__: `!attribute members_stat 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "rules_message": "Permet d'ajouté une petit verification lorsque l'utilisateur rejoin le serveur.\n__Exemple__: `!attribute rules_message 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "create_personal_vocal": "Permet d'ajouté un salon vocaux qui permetera de crée des salons personnalisé\n__Exemple__: `!attribute create_personal_vocal 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "perm_command": "Permet d'attribué des permission lors de l'execution d'une commandes !\n__Exemple__: `!attribute perm_command nickname_member 852576991504105514`"
                    }
                ],
            "ban": [
                """
                Permet de bannir un membre du serveur temporairement ou bien definitif.
                __Exemple__: `!ban <user_id> <time> <raison>`
                **_Uniquement disponible au Propriétaire,Administrateur et Modérateur du serveur._**
                """
                ],
            "bitrate": [
                """
                **Uniquement utilisable dans un salon vocal !**
                Permet de changé le bitrate du salon vocal, par defaut, il est attribué à 64Kbps.
                __Exemple__: `!bitrate <Kbps>`
                """
                ],
            "edit": [
                """
                :white_small_square: `!edit role_emoji`
                :white_small_square: `!edit role_info`
                :white_small_square: `!edit role`
                :white_small_square: `!edit channel`
                :white_small_square: `!edit members_stat`
                :white_small_square: `!edit rules_message`
                :white_small_square: `!edit create_personal_vocal`
                :white_small_square: `!edit perm_command`
                :white_small_square: `!edit nickname_member`
                :white_small_square: `!edit function`
                """,
                {
                    "channel": "Permet de modifier des salons textuels dans la base de donnée",
                    "role_emoji": "Permet de modifier un emoji à chaque rôle !\n__Exemple__: `!edit role_emoji actuality_role 📰`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "role_info": "Permet de modifier plus d'information sur un rôle !\n__Exemple__: `!edit role_info member_role 'Le role par defaut'`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "role": "Permet de modifier l'emoji a un rôle !\n__Exemple__: `!edit role 📰 859421483524423690`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "members_stat": "Permet de modifier un salon vocaux pour affiché le nombre de membres presentement dans le serveur Discord\n__Exemple__: `!edit members_stat 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "rules_message": "Permet de modifier une petit verification lorsque l'utilisateur rejoin le serveur.\n__Exemple__: `!edit rules_message 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "create_personal_vocal": "Permet de modifier un salon vocaux qui permetera de crée des salons personnalisé\n__Exemple__: `!edit create_personal_vocal 852576991504105514`\n**_Destiné uniquement au propriétaire du serveur._**",
                    "perm_command": "Permet de modifier des permission lors de l'execution d'une commandes !\n__Exemple__: `!edit perm_command nickname_member 852576991504105514`"
                    }
                ],
            "get": [
                """
                :white_small_square: `!get info_user`
                :white_small_square: `!get role_attributed`
                """,
                {
                    "info_user": " ",
                    "role_attributed": " "
                    }
                ],
            "send": [
                """
                :white_small_square: `!send custom_message`
                :white_small_square: `!send roles_message`
                :white_small_square: `!send rules_message`
                """,
                {
                    "custom_message": " ",
                    "roles_message": " ",
                    "rules_message": " "
                    }
                ],
            "nickname": [
                """
                **Permet de changé votre pseudo dans ce serveur Discord.**
                __Exemple__: !nickname "<Nouveau-Pseudo>"
                """
                ]
            }

    async def execute(self,ctx,args):
        colour_embed = Colour.from_rgb(96,96,96)
        # !help
        if len(args) == 0:
            help_message = Embed(title="> **Vous avez appelé la commande `!help`.**",color=colour_embed)
            list_commands_msg = """
                    _Commandes destiné au propriétaire_:
                    :white_small_square: `!attribute` _**|**_ `!edit` _**|**_ `!remove`
                    :white_small_square: `!send` _**|**_ `!get`

                    _Commandes destiné au Administration/Modération_:
                    :white_small_square: `!ban` _**|**_ `!unban` _**|**_ `!mute`

                    _Commandes destiné au membre du serveur_:
                    :white_small_square: `!help` _**|**_ `!nickname` _**|**_ `!ping`
                    :white_small_square: `!myvocal`
                    """
            list_alias_msg = """
                    :white_small_square: `!mv` _(== `!myvocal`)_
                    """
            help_message.add_field(name="**Liste des commandes disponible:**",value=list_commands_msg)
            help_message.add_field(name="**Liste des alias:**",value=list_alias_msg)
            help_message.set_footer(text=f"Pour plus d'info, tapez !help <commandes>. Votre serviteur {self.bot.user.name} vous affichera plus de detail",icon_url=self.bot.user.avatar_url)
        # !help <command1>
        if len(args) == 1:
            help_message = Embed(title=f"> **Vous avez appelé la commande `!help {args[0]}`.**",color=colour_embed)
            # Try if there are a wrong command or if is a good command
            try:
                self.commands_info[args[0]][0]
            except (KeyError,IndexError):
                return await ctx.send(embed=Embed(title="> ⚠ **Commande introuvable !**",description="Verifiez l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
            else:
                help_message.add_field(name="**Liste des commandes disponible:**",value=self.commands_info[args[0]][0])
                help_message.set_footer(text=f"Pour plus d'info, tapez !help {args[0]} <commandes>.")
        # !help <command1> <command2>
        if len(args) == 2:
            help_message = Embed(title=f"> **Vous avez appelé la commande `!help {args[0]} {args[1]}`.**",color=colour_embed)
            # Try if there are a wrong command or if is a good command
            try:
                self.commands_info[args[0]][1][args[1]]
            except (KeyError,IndexError):
                return await ctx.send(embed=Embed(title="> ⚠ **Commande introuvable !**",description="Verifiez l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
            else:
                help_message.add_field(name="**Information sur la commande:**",value=self.commands_info[args[0]][1][args[1]])

        help_message.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=help_message)

    @commands.command(name="help")
    async def help_command(self,ctx,*args):
        await self.execute(ctx,args)

