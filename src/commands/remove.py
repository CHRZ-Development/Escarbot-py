import os

from discord.ext import commands

from exceptions.InvalidSubcommand import InvalidSubcommand


class RemoveCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.subcommand = {"roles": self.remove_roles,"channels": self.remove_channels}
        self.refresh_database = lambda: self.bot.file.write(self.bot.guilds_data,"guilds_data.json",f"{os.getcwd()}/res/")
        self.remove.add_check(self.bot.check_permission)

    async def remove_roles(self,ctx,args):
        self.bot.guilds_data[str(ctx.guild.id)]["roles"].pop(int(args[0]))
        self.refresh_database()

    async def remove_channels(self,ctx,args):
        self.bot.guilds_data[str(ctx.guild.id)]["channels"].pop(int(args[0]))
        self.refresh_database()

    @commands.command(name="remove")
    async def remove(self,ctx,option,*args):
        try:
            await self.subcommand[option](ctx,args)
        except KeyError:
            raise InvalidSubcommand(option)
        return await ctx.message.delete()
