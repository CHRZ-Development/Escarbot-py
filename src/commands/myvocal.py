from discord.ext import commands
from discord import Colour,Embed,PermissionOverwrite,utils


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


class MyVocalCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.detail_edit_message = {"rename": lambda ctx,other: f"Votre salon vocal <#{ctx.author.voice.channel.id}> a bien été renommé en `" + " ".join(other) + "`","bitrate": lambda ctx,other: f"Votre salon vocal <#{ctx.author.voice.channel.id}> a bien été régler sur `{other}Kbps`","public": lambda ctx,other: f"La confidentialité de <#{ctx.author.voice.channel.id}> à étais mise sur publique","private": lambda ctx,other: f"La confidentialité de <#{ctx.author.voice.channel.id}> à étais mise sur privée"}
        self.commands = {"rename": self.rename_vocal,"bitrate": self.bitrate_vocal,"public": self.public_vocal,"private": self.private_vocal}

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
    @commands.after_invoke(send_modification)
    async def vocal_command(self,ctx,*args):
        option = args[0]
        try:
            await self.commands[str(option)](ctx,args)
        except KeyError:
            return await ctx.send(embed=Embed(title="> ⚠ **Commande introuvable !**",description="Verifiez l'orthographe !",color=Colour.from_rgb(255,255,0)).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))

