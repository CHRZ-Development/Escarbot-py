from discord import Embed,Forbidden
from discord.ext import commands
from discord.ext.commands import CommandError,Context
from discord_slash import ButtonStyle,ComponentContext,cog_ext,SlashContext
from discord_slash.error import SlashCommandError
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_actionrow,create_button,wait_for_component


class Nickname(object):
    accept_letter = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","[","]","{","}","|","(",")","+","=","°","^","~","&",":",";","/",".",",","!","?","*","%","ù","é","è","à","$","¨"," ","1","2","3","4","5","6","7","8","9","0"]
    success_msg = ["Changement effectué avec :white_check_mark: succès !",lambda value: f"Votre pseudo a été changé par `{value}`"]

    def __init__(self,obj,bot):
        self.obj = obj
        self.bot = bot
        self.error_msg = [["Changement n'a pas pu êtres effectué avec :x: succès !",lambda error: self.bot.translator.translate(src="en",dest="fr",text=str(error)).text],["Votre pseudo doit contenir:","`" + "".join(self.accept_letter) + "`"]]

    async def execute(self,ctx,nickname,action=None):
        """ execute() -> It allow to execute the same code in a simple command and in slash command. """
        for letter in nickname:
            # Have wrong character.
            if str(letter) not in self.accept_letter:
                raise SlashCommandError("The characters specified is not available !") if isinstance(ctx,SlashContext) else CommandError("The characters specified is not available !")
        try:
            await ctx.author.edit(nick=nickname)
        except Forbidden:
            pass
        else:
            return (await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=str(nickname),action=[action]),action) if isinstance(ctx,SlashContext) else await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,value=str(nickname))


class NicknameCommand(Nickname,commands.Cog):
    def __init__(self,bot):
        Nickname.__init__(self,self,bot)
        self.bot = bot

    @commands.command(name="nickname",aliases=["nick","nn"])
    async def nickname_command(self,ctx: Context,new_nickname: str): return await self.execute(ctx,new_nickname)

    @nickname_command.error
    async def nickname_error(self,ctx: Context,error): return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=error)


class NicknameSlash(Nickname,commands.Cog):
    nickname_command_options = [create_option(name="new_nickname",description="Specifié le nouveau pseudo",option_type=3,required=True)]

    def __init__(self,bot):
        Nickname.__init__(self,self,bot)
        self.bot = bot
        self.data = {}

    @cog_ext.cog_slash(name="nickname",description="Permet de changé votre pseudo dans ce serveur Discord.",options=nickname_command_options)
    async def nickname(self,ctx: SlashContext,new_nickname: str):
        # Msg nickname edited successful + "🤭 Une faute ?" Button
        msg,wrong_nickname_action = await self.execute(ctx,nickname=new_nickname,action=create_actionrow(create_button(style=ButtonStyle.red,label="Une faute ?",emoji="🤭")))
        # Wait pressed "🤭 Une faute ?" Buttton
        wrong_button: ComponentContext = await wait_for_component(self.bot,components=wrong_nickname_action)
        # Msg for "🤭 Une faute ?" Button
        wrong_nickname_msg = Embed()
        wrong_nickname_msg.add_field(name="Vous avez appuyé sur le bouton `Une faute ?`.",value="Entrez votre nouveau pseudo !")
        wrong_nickname_msg.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        # Create button "🧐 Tu ne veux plus le changé ?"
        cancel_action = create_actionrow(create_button(style=ButtonStyle.red,label="Tu ne veux plus le changé ?",emoji="🧐"))
        if wrong_button.author == ctx.author:
            # On pressed "🤭 Une faute ?" Button, send message
            await wrong_button.send(embed=wrong_nickname_msg,components=[cancel_action])
        else:
            wrong_user_msg = Embed()
            wrong_user_msg.add_field(name="⚠ Utilisateur non autorisé",value="Vous n'etes pas autorisé d'appuie sur ce bouton !")
            wrong_user_msg.set_author(name=wrong_button.author.name,icon_url=wrong_button.author.avatar_url)
            return await wrong_button.send(embed=wrong_user_msg)
        # Enable nickname process function
        self.data[str(ctx.author.id)] = [True,True]
        # Wait pressed "🧐 Tu ne veux plus le changé ?" Button
        cancel_button: ComponentContext = await wait_for_component(self.bot,components=cancel_action)
        if self.data[str(ctx.author.id)][1]:
            # Msg for "🧐 Tu ne veux plus le changé ?"
            button_msg_final = Embed()
            button_msg_final.add_field(name="Vous avez appuyé sur le bouton `Tu ne veux plus le changé ?`.",value="Vous avez fermez la possibilité de changé votre pseudo du a une faute de frappe ou bien d'un mauvais pseudo.\nVous pouvez toujours executé la commande `/nickname` apres ca.")
            button_msg_final.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
            button_msg_final.set_footer(text=self.bot.success_footer[0],icon_url=self.bot.user.avatar_url)
            # On pressed "🧐 Tu ne veux plus le changé ?" Button, send message
            await cancel_button.send(embed=button_msg_final)
        # Cancel nickname process msg
        self.data[str(ctx.author.id)] = [False,False]

    @nickname.error
    async def nickname_error(self,ctx: SlashContext,error): return await self.bot.send_message_after_invoke(ctx,self.success_msg,self.error_msg,error=error)

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
                    nickname = message.content
                    # Check letter per letter.
                    for letter in nickname:
                        # Have wrong character.
                        if str(letter) not in self.accept_letter:
                            self.data[str(message.author.id)] = [False,False]
                            raise SlashCommandError("The characters specified is not available !")
                    self.data[str(message.author.id)] = [False,False]
                    try:
                        await message.author.edit(nick=nickname)
                        return await self.bot.send_message_after_invoke(message,self.success_msg,self.error_msg,value=nickname)
                    except Forbidden:
                        pass
