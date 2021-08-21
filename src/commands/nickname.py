from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import ButtonStyle,cog_ext,SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_actionrow,create_button


class Nickname(commands.Cog):
    accept_letter = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","[","]","{","}","|","(",")","+","=","°","^","~","&",":",";","/",".",",","!","?","*","²","%","ù","é","è","à","$","€","¨"," ","1","2","3","4","5","6","7","8","9","0"]
    success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Votre pseudo a été changé par `{value}`"]
    data = {}

    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
        self.obj.nickname.add_check(self.good_char)

    async def good_char(*args):
        if isinstance(args[1],SlashContext):
            nickname = args[1].args
        else:
            tmp = str(args[1].message.content).split(" ")
            nickname = tmp[1]
        for letter in nickname[0]:
            # Have wrong character.
            if str(letter) not in args[0].accept_letter:
                raise Exception("The characters specified is not available !")
        return True

    async def execute(self,ctx,nickname,action=None):
        """ execute() -> It allow to execute the same code in a simple command and in slash command. """
        await ctx.author.edit(nick=nickname)
        return (await self.bot.send_message_after_invoke(ctx,self.success_msg,[],value=str(nickname),action=[action]),action) if action is not None else await self.bot.send_message_after_invoke(ctx,self.success_msg,[],value=str(nickname))

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot is False:
            try:
                self.data[str(message.author.id)]
            except KeyError:
                pass
            else:
                # Nickname system process
                if self.data[str(message.author.id)][0]:
                    # Check letter per letter.
                    for letter in message.content:
                        # Have wrong character.
                        if str(letter) not in self.accept_letter:
                            self.data[str(message.author.id)] = [False,False]
                            return
                    self.data[str(message.author.id)] = [False,False]
                    await message.author.edit(nick=message.content)
                    return await self.bot.send_message_after_invoke(message,self.success_msg,[],value=message.content)


class NicknameCommand(Nickname,commands.Cog):
    def __init__(self,bot):
        Nickname.__init__(self,self,bot)
        self.bot = bot

    @commands.command(name="nickname",aliases=["nick","nn"])
    async def nickname(self,ctx: Context,new_nickname):
        msg,wrong_nickname_action = await self.execute(ctx,nickname=new_nickname,action=create_actionrow(create_button(style=ButtonStyle.red,label="Une faute ?",emoji="🤭")))
        return await self.bot.can_rename_after_invoke_command(self,ctx,wrong_nickname_action)


class NicknameSlash(Nickname,commands.Cog):
    nickname_command_options = [create_option(name="new_nickname",description="Specifié le nouveau pseudo",option_type=3,required=True)]

    def __init__(self,bot):
        Nickname.__init__(self,self,bot)
        self.bot = bot

    @cog_ext.cog_slash(name="nickname",description="Permet de changé votre pseudo dans ce serveur Discord.",options=nickname_command_options)
    async def nickname(self,ctx: SlashContext,new_nickname: str):
        msg,wrong_nickname_action = await self.execute(ctx,nickname=new_nickname,action=create_actionrow(create_button(style=ButtonStyle.red,label="Une faute ?",emoji="🤭")))
        return await self.bot.can_rename_after_invoke_command(self,ctx,wrong_nickname_action)
