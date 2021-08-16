from discord.ext import commands
from discord import PermissionOverwrite
from discord.ext.commands import CheckFailure,CommandError
from discord_slash import SlashContext,cog_ext,error
from discord_slash.utils.manage_commands import create_option


class MyVocal(object):
    success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Les parametres de votre vocal à été changé ! Parametre modifié 👉 `{value}`"]

    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
        self.error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda _error: self.bot.translator.translate(src="en",dest="fr",text=str(_error)).text]]

    def set_permissions(self):
        perms = PermissionOverwrite()
        perms.manage_channels = True
        perms.manage_roles = True
        perms.connect = True
        return perms

    def set_confidentiality(self,connect):
        perms = PermissionOverwrite()
        perms.connect = connect
        return perms

    async def bitrate_vocal(self,ctx,kbps): return await ctx.author.voice.channel.set_permissions(ctx.author,overwrite=self.set_permissions()),await ctx.author.voice.channel.edit(bitrate=kbps*1000)

    async def rename_vocal(self,ctx,name): return await ctx.author.voice.channel.set_permissions(ctx.author,overwrite=self.set_permissions()),await ctx.author.voice.channel.edit(name=name)

    async def error_vocal(self,ctx,_error): return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.obj.error_msg,error="You are not in vocal !\n You need to create or join a vocal.") if isinstance(_error,error.CheckFailure) or isinstance(_error,CheckFailure) else await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=_error)

    async def public_vocal(self,ctx): return await ctx.author.voice.channel.set_permissions(ctx.author.roles[0],overwrite=self.set_confidentiality(True))

    async def private_vocal(self,ctx): return await ctx.author.voice.channel.set_permissions(ctx.author.roles[0],overwrite=self.set_confidentiality(False))


class MyVocalCommand(MyVocal,commands.Cog):
    def __init__(self,bot):
        MyVocal.__init__(self,self,bot)
        self.bot = bot
        self.subcommands = {"rename": self.rename_vocal,"bitrate": self.bitrate_vocal,"public": self.public_vocal,"private": self.private_vocal}

    @commands.command(name="myvocal",aliases=["mv"])
    async def vocal_command(self,ctx,option: str,value: str=None):
        try:
            self.subcommands[option]
        except KeyError:
            raise CommandError("This option isn't exist !")
        else:
            if value is not None:
                await self.subcommands[option](ctx,value)
                return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=value)
            await self.subcommands[option](ctx)
            return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=f"Confidentialité: {option}")

    @vocal_command.add_check
    async def vocal_command_check(*args): return True if args[0].author.voice is not None else False

    @vocal_command.error
    async def vocal_command_error(self,ctx,_error): await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=_error) if isinstance(ctx,error.CheckFailure) or isinstance(ctx,CheckFailure) else await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error="You are not in a vocal channel !\nYou need to create or join a vocal channel.")


class MyVocalSlash(MyVocal,commands.Cog):
    base_command_info = ["myvocal","Permet de modifié plusieurs parametre de votre salon"]
    bitrate_subcommand_option = [create_option(name="kbps",description="Specifié la valeurs en Kbps",option_type=4,required=True)]
    rename_subcommand_option = [create_option(name="nom",description="Specifié votre nouveau nom de votre salon vocal",option_type=3,required=True)]
    success_msg_details = {"bitrate": lambda kbps: f"bitrate: {kbps} Kbps","rename": lambda nom: f"nom: {nom}","public": "Confidentialité: publique","private": f"Confidentialité: privée"}

    def __init__(self,bot):
        MyVocal.__init__(self,self,bot)
        self.bot = bot

    async def execute(self,ctx,func,value=None):
        if value is not None:
            await func(ctx,value)
            return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=self.success_msg_details[ctx.subcommand_name](value))
        await func(ctx)
        return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=self.success_msg_details[ctx.subcommand_name])

    @cog_ext.cog_subcommand(base=base_command_info[0],name="bitrate",base_desc=base_command_info[1],description="Permet de modifié le bitrate (En Kbps) votre salon vocal",options=bitrate_subcommand_option)
    async def myvocal_bitrate(self,ctx: SlashContext,kbps: int): return await self.execute(ctx,self.bitrate_vocal,value=kbps)

    @cog_ext.cog_subcommand(base=base_command_info[0],name="rename",base_desc=base_command_info[1],description="Permet de modifié le nom de votre salon vocal",options=rename_subcommand_option)
    async def myvocal_rename(self,ctx: SlashContext,nom: str): return await self.execute(ctx,self.rename_vocal,value=nom)

    @cog_ext.cog_subcommand(base=base_command_info[0],name="public",base_desc=base_command_info[1],description="Permet de rendre votre vocal en publique")
    async def myvocal_public(self,ctx: SlashContext): return await self.execute(ctx,self.public_vocal)

    @cog_ext.cog_subcommand(base=base_command_info[0],name="private",base_desc=base_command_info[1],description="Permet de rendre votre vocal en privée")
    async def myvocal_private(self,ctx: SlashContext): return await self.execute(ctx,self.private_vocal)

    @myvocal_bitrate.add_check
    async def myvocal_check(*args): return True if args[0].author.voice is not None else False

    @commands.Cog.listener()
    async def on_slash_command_error(self,ctx,_error): await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=_error) if isinstance(ctx,error.CheckFailure) or isinstance(ctx,CheckFailure) else await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error="You are not in a vocal channel !\nYou need to create or join a vocal channel.")
