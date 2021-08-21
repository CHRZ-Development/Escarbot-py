from discord.ext import commands
from discord import PermissionOverwrite
from discord.ext.commands import Context
from discord_slash import ButtonStyle,SlashContext,cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_actionrow,create_button


class MyVocal(commands.Cog):
    success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Les parametres de votre vocal à été changé ! Parametre modifié 👉 `{value}`"]
    data = {}

    def __init__(self,obj,bot,funcs: list):
        self.obj = obj
        self.bot = bot
        self.subcommands = {"rename": self.rename_vocal,"bitrate": self.bitrate_vocal,"public": self.public_vocal,"private": self.private_vocal}
        for func in funcs:
            func.add_check(self.myvocal_check)

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

    async def myvocal_check(*args): return args[1].author.voice is not None

    async def bitrate_vocal(self,ctx,kbps):
        voice_channel = ctx.author.voice.channel
        await voice_channel.set_permissions(ctx.author,overwrite=self.set_permissions())
        await voice_channel.edit(bitrate=int(kbps)*1000)

    async def rename_vocal(self,ctx,name):
        voice_channel = ctx.author.voice.channel
        await voice_channel.set_permissions(ctx.author,overwrite=self.set_permissions())
        await voice_channel.edit(name=str(name))

    async def public_vocal(self,ctx): await ctx.author.voice.channel.set_permissions(ctx.author.roles[0],overwrite=self.set_confidentiality(True))

    async def private_vocal(self,ctx): await ctx.author.voice.channel.set_permissions(ctx.author.roles[0],overwrite=self.set_confidentiality(False))

    async def execute(self,ctx,option,value=None,action=None):
        try:
            self.subcommands[option]
        except KeyError:
            raise Exception("This subcommand isn't exist !")
        else:
            await self.subcommands[option](ctx) if value is None else await self.subcommands[option](ctx,value)
            await self.bot.send_message_after_invoke(ctx,self.success_msg,[],value=f"Confidentialité: {option}" if value is None else value,action=action)
            if action is not None:
                await self.bot.can_rename_after_invoke_command(self,ctx,action)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot is False:
            try:
                self.data[str(message.author.id)]
            except KeyError:
                pass
            else:
                if self.data[str(message.author.id)][0]:
                    voice_channel = message.author.voice.channel
                    await voice_channel.set_permissions(message.author,overwrite=self.set_permissions())
                    await voice_channel.edit(name=str(message.content))
                    await self.bot.send_message_after_invoke(message,self.success_msg,[],value=str(message.content))


class MyVocalCommand(MyVocal,commands.Cog):
    def __init__(self,bot):
        MyVocal.__init__(self,self,bot,[self.vocal_command])
        self.bot = bot

    @commands.command(name="myvocal",aliases=["mv"])
    async def vocal_command(self,ctx: Context,subcommand,value=None): await self.execute(ctx,subcommand,value=value,action=[create_actionrow(create_button(style=ButtonStyle.red,label="Une faute ?",emoji="🤭"))]) if subcommand == "rename" else await self.execute(ctx,subcommand,value=value)


class MyVocalSlash(MyVocal,commands.Cog):
    base_command_info = ["myvocal","Permet de modifié plusieurs parametre de votre salon"]
    bitrate_subcommand_option = [create_option(name="kbps",description="Specifié la valeurs en Kbps",option_type=4,required=True)]
    rename_subcommand_option = [create_option(name="nom",description="Specifié votre nouveau nom de votre salon vocal",option_type=3,required=True)]
    success_msg_details = {"bitrate": lambda kbps: f"bitrate: {kbps} Kbps","rename": lambda nom: f"nom: {nom}","public": "Confidentialité: publique","private": f"Confidentialité: privée"}

    def __init__(self,bot):
        MyVocal.__init__(self,self,bot,[self.myvocal_bitrate,self.myvocal_rename,self.myvocal_public,self.myvocal_private])
        self.bot = bot

    @cog_ext.cog_subcommand(base=base_command_info[0],name="bitrate",base_desc=base_command_info[1],description="Permet de modifié le bitrate (En Kbps) votre salon vocal",options=bitrate_subcommand_option)
    async def myvocal_bitrate(self,ctx: SlashContext,kbps): return await self.execute(ctx,"bitrate",value=kbps)

    @cog_ext.cog_subcommand(base=base_command_info[0],name="rename",base_desc=base_command_info[1],description="Permet de modifié le nom de votre salon vocal",options=rename_subcommand_option)
    async def myvocal_rename(self,ctx: SlashContext,nom): return await self.execute(ctx,"rename",value=nom,action=[create_actionrow(create_button(style=ButtonStyle.red,label="Une faute ?",emoji="🤭"))])

    @cog_ext.cog_subcommand(base=base_command_info[0],name="public",base_desc=base_command_info[1],description="Permet de rendre votre vocal en publique")
    async def myvocal_public(self,ctx: SlashContext): return await self.execute(ctx,"public")

    @cog_ext.cog_subcommand(base=base_command_info[0],name="private",base_desc=base_command_info[1],description="Permet de rendre votre vocal en privée")
    async def myvocal_private(self,ctx: SlashContext): return await self.execute(ctx,"private")
