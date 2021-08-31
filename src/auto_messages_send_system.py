import datetime

from discord.ext import commands
from discord import Colour,Embed,HTTPException,Member,utils,Forbidden,NotFound
from discord.ext.commands import has_permissions


class AutoMessagesSendSystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def detect_role_changed(self,b,a):
        """ detect_role_changed( ) -> Notify hierarchical change
                :param b: before
                :param a: after """
        try:
            # Text Channel
            channel_lvlup = self.bot.get_channel(self.bot.guilds_data[str(b.guild.id)]["channels_ID"]["lvl_up"])
        except KeyError:
            return
        else:
            b_role,a_role = {},{}
            # If the roles at been changed
            if a.roles != b.roles:
                # Write all role between after and before role attribute
                number_keys_b_role,number_keys_a_role = 0,0
                for role in b.roles:
                    b_role[role.name] = role
                    number_keys_b_role += 1
                for role in a.roles:
                    a_role[role.name] = role
                    number_keys_a_role += 1
                # If after attribute role as been changed
                if number_keys_a_role > number_keys_b_role:
                    change_role = a_role
                    compare_role = b_role
                else:
                    # Stop this function
                    return
                # Detect the new name of role
                role_update = None
                for role in change_role:
                    try:
                        compare_role[role]
                    except KeyError:
                        role_update = role
                # Send the hierarchical changed
                level_up_message = Embed(title="> __**Niveau superieurs !**__",colour=Colour.from_rgb(102,255,255))
                level_up_message.add_field(name="**Vous avez eu un niveau superieurs**",value=f"Vous avez maintenant le rôle `{role_update}`.")
                level_up_message.set_author(name=a.name,icon_url=a.avatar_url)
                get_role = utils.get(a.guild.roles,name=role_update)
                if get_role.id == int(self.bot.guilds_data[str(a.guild.id)]["roles"][0]["role_id"]):
                    await self.welcome_message(a)
                return await channel_lvlup.send(embed=level_up_message)

    async def welcome_message(self,member):
        text_channel = self.bot.get_channel(int(self.bot.guilds_data[str(member.guild.id)]["channels_ID"]["welcome_channel"]))
        welcome_message = Embed(description=f"Je te souhaite la bienvenue {member.mention} ! Prend un ☕ café et vient dans <#839042197629304853>, dit nous coucou !",colour=Colour.from_rgb(0,128,255))
        welcome_message.set_author(name=member.name,icon_url=member.avatar_url)
        print(f"[{datetime.datetime.today().date()}] L'utilisateur {member.name} est arrivée dans le serveur !")
        await text_channel.send(embed=welcome_message)

    async def create_vocal_message(self,member):
        text_channel = self.bot.get_channel(int(self.bot.guilds_data[str(member.guild.id)]["channels_ID"]["command_channel"]))
        create_vocal_message = Embed(title="> **Vous venez de crée un salon vocal !**",colour=Colour.from_rgb(96,96,96))
        create_vocal_message.add_field(name=f"Vous avez droit désormais grâce à votre salon:",value="Commandes:\n:white_small_square: `!myvocal` _(alias `!mv`)_\n:white_small_square: `/myvocal`\n_Pour plus d'info sur les commandes, entrez `!help <commande>`_\n\n:white_small_square: Ecouté de la <#867173777485725706>\n_Pour plus d'info sur le Bot musique, entrez `.help`_")
        create_vocal_message.set_author(name=member.name,icon_url=member.avatar_url)
        create_vocal_message.set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url)
        await text_channel.send(embed=create_vocal_message)

    async def ban_message(self,guild,member: Member,how_much_days,why):
        # if a channel is attributed
        ban_message = Embed(title="> Oh ! Un ban... 🤨",color=Colour.from_rgb(255,0,0))
        msg_days_info = f"pour **{how_much_days} jours**" if self.bot.users_data[str(guild.id)][str(member.id)]["CriminalRecord"]["BanInfo"]["Definitive"] is False else "**définitivement**"
        # Text channel message
        ban_message.add_field(name=f"L'utilisateur {member.name} à étais banni·e",value=f"Banni·e {msg_days_info} pour avoir `{why}`")
        ban_message.set_author(name=member.name,icon_url=member.avatar_url)
        ban_message.set_image(url="https://media.giphy.com/media/l2Sqh1SNVIaVKzWVy/giphy.gif")
        # MP Message
        mp_ban_message = Embed(title=f"> Vous etes banni·e du serveur {guild.name}",color=Colour.from_rgb(255,0,0))
        mp_ban_message.add_field(name="__Information du ban__:", value=f"Vous etes banni·e {msg_days_info} pour avoir `{why}`")
        mp_ban_message.set_author(name=guild.name,icon_url=guild.icon_url)
        mp_ban_message.set_footer(text=member.name,icon_url=member.avatar_url)
        # Ticket message
        mp_ticket_message = Embed(title="> **Vous trouvez ce ban injustifiée ?**",colour=Colour.from_rgb(255,0,0))
        mp_ticket_message.add_field(name="Voici un Discord pour pouvoir êtres en relaxion avec un membre du staff",value="__https://discord.gg/Se2phANYrG__")
        mp_ticket_message.set_footer(text=f"Signé {guild.owner.name}.",icon_url=guild.owner.avatar_url)
        try:
            await member.send(embed=mp_ban_message)
            await member.send(embed=mp_ticket_message)
        except Forbidden:
            print(f"[{datetime.datetime.today().date()}] L'utilisateur {member.name} n'a pas pu·e êtres prevenu de sont ban")
        try:
            text_channel = utils.get(guild.text_channels,id=self.bot.guilds_data[str(guild.id)]["channels_ID"]["criminal_report"])
        except KeyError:
            pass
        else:
            await text_channel.send(embed=ban_message)

    async def unban_message(self,guild,member):
        # MP Message
        mp_unban_message = Embed(title=f"> Vous etes unban du serveur {guild.name}",color=Colour.from_rgb(255,0,0))
        mp_unban_message.add_field(name="__Information du unban__:",value=f"Vous etes plus banni·e du serveur Discord !")
        mp_unban_message.set_author(name=guild.name,icon_url=guild.icon_url)
        mp_unban_message.set_footer(text=member.name,icon_url=member.avatar_url)
        try:
            await member.send(embed=mp_unban_message)
        except Forbidden:
            print(f"[{datetime.datetime.today().date()}] L'utilisateur {member.name} n'a pas pu·e êtres prevenu de sont unban")

    async def message_from_url_discord(self,message):
        if message.author.bot is False:
            message_content,*message_url = str(message.content).split('/')
            # Stock messages
            final_messages = []
            try:
                message_url[1]
            except (KeyError,IndexError):
                return
            # discord.com/channels
            # If URL contain "discord.com" and "channels"
            if (message_url[1] == "discord.com") and (message_url[2] == "channels"):
                # discord.com/channels/<guild_id>/<text_channel>
                text_channel = self.bot.get_channel(int(message_url[4]))
                try:
                    # discord.com/channels/<guild_id>/<text_channel>/<msg_id>
                    # Try to found the message in the guild
                    msg = await text_channel.fetch_message(int(message_url[5]))
                except NotFound:
                    return
                else:
                    # If contain multiple Embeds
                    if len(msg.embeds) >= 1:
                        for n,embed in enumerate(msg.embeds):
                            final_messages.append(Embed(title=str(embed.title),description=str(embed.description)))
                            for field in embed.fields:
                                final_messages[n].add_field(name=field.name,value=field.value,inline=field.inline)
                            final_messages[n].set_footer(text=f"Le message a été publié sur {text_channel.name} dans {message.guild.name}. | Posté le {msg.created_at.date()}",icon_url=msg.guild.icon_url)
                    else:
                        try:
                            msg_tmp = Embed().add_field(name=f"Message posté le {msg.created_at.date()}",value=msg.content)
                        except HTTPException:
                            msg_tmp = Embed(description=msg.content)
                        final_messages.append(msg_tmp)
                        final_messages[0].set_footer(text=f"Le message a été publié sur {text_channel.name} dans {message.guild.name}.",icon_url=msg.guild.icon_url)
                    filename = []
                    for att in msg.attachments:
                        filename.append(str(att.proxy_url))
                    # Send message
                    for n,embd in enumerate(final_messages):
                        embd.set_author(name=msg.author.name,icon_url=msg.author.avatar_url)
                        try:
                            if isinstance(filename[n],str):
                                embd.set_image(url=filename[n])
                        except IndexError:
                            pass
                        await message.channel.send(embed=embd)

    async def on_guild_message(self,guild):
        guild_message = Embed(colour=Colour.from_rgb(0,0,0),description="Merci d'avoir choisi·e Escarbot !")
        guild_message.set_author(name="Escarbot est dans la place !",icon_url=self.bot.user.avatar_url)
        guild_message.set_image(url="https://eapi.pcloud.com/getpubthumb?code=XZncd0Z7XdcnA9yc54RdH5VX8AnE80DFJrX&linkpassword=undefined&size=1599x305&crop=0&type=auto")
        guild_message.add_field(name="⚪ Fiabilité:",value="Ce bot ne vous garantit par une fiabilité à 100%, si vous n'avez pas confiance à ce bot, dirigez-vous sur un bot certifié et plus fiable.\nCeci est un petit projet 'freelance'. Pour plus de [details](https://github.com/NaulaN/Escarbot-py#-fiabilit%C3%A9)",inline=False)
        guild_message.add_field(name="⚪ Wiki:",value="Pour plus de détails, vous avez droit au [Wiki.](https://github.com/NaulaN/Escarbot-py/wiki)",inline=False)
        guild_message.add_field(name="⚪ Hébergement du Bot:",value="Ce bot est hébergé chez un domicile donc, ne garantit en aucun cas d'un fonctionnement 24h/24 et 7j/7\nDonc, il pourrait avoir des arrêts d'hébergement du serveur, une ou deux sur quelques mois (donc peu de coupure), les coupures peuvent durée entre quelques minutes ou bien quelques jours\nC'est coupure peut être prévu par le développer\n Si jamais le Bot est inactif depuis plus 1 mois, contactez-le [developer](https://discord.gg/yEvBg8CPaM) ! Il vous dira plus d'informations sur la coupure.",inline=False)
        guild_message.add_field(name="⚪ Bot sous licence !",value="Ce bot est sous licence MIT.\nPour plus d'information sur la [Licence.](https://github.com/NaulaN/Escarbot-py/blob/master/LICENSE) 👀",inline=False)
        guild_message.add_field(name="⚪ Conseil:",value="Invitez des membres si vous avez terminé votre à 100% serveur, pas avant !\nDe plus, plusieurs personnes font cette erreur, ne le faite surtout pas !\nEn conclusion, il pourrait avoir de nombreux soucis si vous invitez des gens sans que le serveur soit terminé.",inline=False)
        guild_message.add_field(name="⚪ Aide rapide:",value="Vous pouvez execute la commande `!help` ou bien `/help` pour avoir une documentation rapide non détaillé")
        guild_message.set_footer(text="Copyright (c) 2021 CHRZ Developement",icon_url="https://avatars.githubusercontent.com/u/67024770?s=400&u=24615cb4001020dbe7900d45f8c85a9c3c5d0725&v=4")
        await guild.system_channel.send(embed=guild_message)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"|=------------------------------------------------=|")
        print(f"| - ✅ Est lancée depuis {datetime.datetime.today().date()}")
        print(f"| - 🤖 Bot: {self.bot.user.name}")
        print(f"| - 🟢 Connecté sur: {len(self.bot.guilds)} serveurs")
        print(f"|=------------------------------------------------=|")
        print(f"[{datetime.datetime.today().date()}] Je suis prêt ! 👌")

    @commands.Cog.listener()
    async def on_guild_join(self,guild): await self.on_guild_message(guild)

    @commands.Cog.listener()
    async def on_member_ban(self,guild,user): print(f"[{datetime.datetime.today().date()}] L'utilisateur {user.name} à étais ban")

    @commands.Cog.listener()
    async def on_member_unban(self,guild,user):
        print(f"[{datetime.datetime.today().date()}] L'utilisateur {user.name} à étais unban")
        await self.unban_message(guild,user)

    @commands.Cog.listener()
    @has_permissions(manage_roles=True)
    async def on_member_update(self,before,after): await self.detect_role_changed(before,after)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if before.channel is not None:
            if int(before.channel.id) == int(self.bot.guilds_data[str(member.guild.id)]["vocals_ID"]["create_vocal"]):
                await self.create_vocal_message(member)

    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        if str(ctx.command.name) == "ban":
            command,*args = str(ctx.message.content).split(" ")
            member,how_much_days,why = args
            await self.ban_message(ctx.guild,member,how_much_days,why)
        if str(ctx.command.name) in ["warning","warn"]:
            pass
        if str(ctx.command.name) == "mute":
            pass

    @commands.Cog.listener()
    async def on_message(self,message): await self.message_from_url_discord(message)
