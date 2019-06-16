import discord
from discord.ext import commands

import user_db
import config

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        user_id = str(ctx.author.id)
        user_name = ctx.author.name

        if not user_db.check_user(user_id):
            user_db.add_user(user_id, user_name)

            embed = discord.Embed(
                title="**Terms of Use**",
                url='https://github.com/ilmango-doge/Tip-Sugar/blob/master/README.md#terms',
                color=0x0043ff)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="Please read all contents of README, __**especially Terms**__.",
                value="__If you use any command after this message, I will understand that as acceptance of the terms and conditions.__")
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
        else:
            pass

            embed = discord.Embed(
                title="**GitHub README**",
                url='https://github.com/ilmango-doge/Tip-Sugar/blob/master/README.md',
                color=0x0043ff)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="Please check usage at the above link.",
                value=" :mag: ")
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.remove_command('help') # remove inital help command
    bot.add_cog(Help(bot))