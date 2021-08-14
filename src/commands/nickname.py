from discord import Embed
from discord.ext import commands


class NicknameCommand(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.accept_letter = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
                              "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                              "[","]","{","}","|","(",")","+","=","°","^","~","&",":",";","/",".",",","!","?","*","%","ù","é","è","à","$","¨"," ",
                              "1","2","3","4","5","6","7","8","9","0"]

    async def message_after_invoke(self,ctx,status,author,nickname):
        msg = Embed()
        if status == "success":
            msg.add_field(name="Changement effectué avec :white_check_mark: succès !",value="Votre pseudo a bien été changé par " + "".join(nickname))
            msg.set_footer(text="Effectué avec succès grâce à Escarbot, votre serviteur !",icon_url=self.bot.user.avatar_url)
        else:
            msg.add_field(name="Changement n'a pas pu êtres effectué avec :x: succès !",value="Votre pseudo a pas été changé par " + "".join(nickname))
            msg.add_field(name="Votre pseudo doit contenir:",value="`" + "".join(self.accept_letter) + "`",inline=False)
            msg.set_footer(text="Escarbot n'a pas pu effectué votre demande !",icon_url=self.bot.user.avatar_url)
        msg.set_author(name=author.name,icon_url=author.avatar_url)
        return await ctx.send(embed=msg)

    @commands.command(name="nickname",aliases=["nick"])
    async def nickname_command(self,ctx,*nickname):
        check = []
        for n,nick in enumerate(nickname):
            for letter in nick:
                if letter not in self.accept_letter:
                    check.append(False)
                check.append(True)
        if check.count(False) == 0:
            await self.message_after_invoke(ctx,"success",ctx.author,nickname)
            return await ctx.author.edit(nick="".join(nickname))
        return await self.message_after_invoke(ctx,"nop",ctx.author,nickname)

