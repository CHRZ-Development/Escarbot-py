from discord.ext import commands
from discord import Colour,Embed,Member,utils
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
                    return False
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
                return await channel_lvlup.send(embed=level_up_message)

    async def check_user_booster(self,b: Member,a: Member):
        if b.premium_since == a.premium_since:
            return False
        guild = utils.get(self.bot.guilds,id=a.guild_id)
        if a.premium_since is None:
            return await a.remove_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))
        channel_lvlup = self.bot.get_channel(self.bot.ids[a.guild.id]["id_channel_lvlup"])
        await a.add_roles(self.bot.get_role(guild,self.bot.ids[a.guild.id]["id_role_booster"]))
        await channel_lvlup.send(embed=self.bot.create_embed("> __**Wow !**__",f"_ _\n**Merci** {a.mention} **d'avoir boost le serveur !** ❤ ! Vous avez maintenant accès à des avantages !\n_ _",0xff80c0))

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        pass

    @commands.Cog.listener()
    @has_permissions(manage_roles=True)
    async def on_member_update(self,before,after):
        await self.detect_role_changed(before,after)
        await self.check_user_booster(before,after)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,event):
        pass

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        pass

