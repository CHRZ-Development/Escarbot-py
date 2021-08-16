from discord.ext import commands
from discord import Colour,Embed,PermissionOverwrite,utils
from discord.ext.commands import CommandError,Context
from discord_slash import SlashContext,cog_ext
from discord_slash.error import SlashCommandError
from discord_slash.utils.manage_commands import create_option


def set_permissions():
    perms = PermissionOverwrite()
    perms.manage_channels = True
    perms.manage_roles = True
    perms.connect = True
    return perms


def set_confidentiality(connect):
    perms = PermissionOverwrite()
    perms.connect = connect
    return perms


async def in_voice_check(ctx,args):
    vocal_channel = ctx.author.voice
    if vocal_channel is not None:
        return True
    raise SlashCommandError("Vous n'etes pas dans un salon vocal !")


async def bitrate_vocal(ctx,kbps):
    await ctx.author.voice.channel.set_permissions(ctx.author,overwrite=set_permissions())
    await ctx.author.voice.channel.edit(bitrate=kbps*1000)


class MyVocalCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Les parametres de votre vocal à été changé ! Parametre modifié 👉 `{value}`"]
        self.error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda error: self.bot.translator.translate(src="en",dest="fr",text=str(error)).text]]
        self.detail_edit_message = {"rename": lambda ctx,other: f"Votre salon vocal <#{ctx.author.voice.channel.id}> a bien été renommé en `" + " ".join(other) + "`","bitrate": lambda ctx,other: f"Votre salon vocal <#{ctx.author.voice.channel.id}> a bien été régler sur `{other}Kbps`","public": lambda ctx,other: f"La confidentialité de <#{ctx.author.voice.channel.id}> à étais mise sur publique","private": lambda ctx,other: f"La confidentialité de <#{ctx.author.voice.channel.id}> à étais mise sur privée"}
        self.subcommands = {"rename": self.rename_vocal,"bitrate": bitrate_vocal,"public": self.public_vocal,"private": self.private_vocal}

    async def check_if_joined_in_vocal(self,ctx):
        vocal_channel = ctx.author.voice
        if vocal_channel is not None:
            vocal_channel = ctx.author.voice.channel
            if vocal_channel.id not in [int(self.bot.guilds_data[str(ctx.guild.id)]["vocals_ID"]["create_vocal"])]:
                await vocal_channel.set_permissions(ctx.author,overwrite=set_permissions())
                return True,vocal_channel
        await ctx.send(embed=Embed(title="> ⚠ **Vous n'etes pas dans un salon !**",description="Vous ne pouvez executé cette commande car vous n'avez pas <#868456252685045760>",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url).set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url))
        return False,None

    async def send_modification(self,*args):
        ctx = args[0]
        try:
            command,option,*other = str(ctx.message.content).split(" ")
        except ValueError:
            command,option = str(ctx.message.content).split(" ")
            other = None
        send_modification_message = Embed(colour=Colour.from_rgb(52,255,52))
        send_modification_message.add_field(name=f"Changement effectué avec **✅ succès** !",value=self.detail_edit_message[option](ctx,other))
        send_modification_message.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        send_modification_message.set_footer(text=f"Effectué avec succès grâce à {self.bot.user.name}, votre serviteur !",icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=send_modification_message)

    async def rename_vocal(self,ctx,args):
        in_vocal,vocal_channel = await self.check_if_joined_in_vocal(ctx)
        if in_vocal:
            await vocal_channel.edit(name=args[1])

    async def bitrate_vocal(self,ctx,args):
        in_vocal,vocal_channel = await self.check_if_joined_in_vocal(ctx)
        if in_vocal:
            await vocal_channel.edit(bitrate=int(args[1])*1000)

    async def public_vocal(self,ctx,args):
        in_vocal,vocal_channel = await self.check_if_joined_in_vocal(ctx)
        if in_vocal:
            everyone = utils.get(ctx.author.guild.roles,id=self.bot.guilds_data[str(ctx.author.guild.id)]["roles"]["🌐"])
            await vocal_channel.set_permissions(everyone,overwrite=set_confidentiality(True))

    async def private_vocal(self,ctx,args):
        in_vocal,vocal_channel = await self.check_if_joined_in_vocal(ctx)
        if in_vocal:
            everyone = utils.get(ctx.author.guild.roles,id=self.bot.guilds_data[str(ctx.author.guild.id)]["roles"]["🌐"])
            await vocal_channel.set_permissions(everyone,overwrite=set_confidentiality(False))

    @commands.command(name="myvocal",aliases=["mv"])
    @commands.check(in_voice_check)
    async def vocal_command(self,ctx,option,value):
        try:
            await self.subcommands[option](ctx,value)
        except KeyError:
            raise CommandError("This option isn't exist !")

    @commands.Cog.listener()
    async def on_command_error(self,ctx: Context,error):
        pass


class MyVocalSlash(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Les parametres de votre vocal à été changé ! Parametre modifié 👉 `{value}`"]
        self.error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda error: self.bot.translator.translate(src="en",dest="fr",text=str(error)).text]]

    @cog_ext.cog_subcommand(base="myvocal",base_description="Permet de modifié plusieurs parametre de votre salon",
                            name="bitrate",description="Permet de modifié le bitrate (En Kbps) votre salon vocal",
                            options=[create_option(name="kbps",description="Specifié la valeurs en Kbps",option_type=4,required=True)])
    async def myvocal_bitrate(self,ctx: SlashContext,kbps: int): return await bitrate_vocal(ctx,kbps)

    @myvocal_bitrate.add_check
    async def myvocal_bitrate_check(self,ctx: SlashContext,kbps: int):
        vocal_channel = ctx.author.voice
        if vocal_channel is not None:
            return True
        raise SlashCommandError("Vous n'etes pas dans un salon vocal !")

    @myvocal_bitrate.error
    async def myvocal_bitrate_error(self,ctx: SlashContext,error): return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=error)
