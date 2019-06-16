from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config

# connect to coind
rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

class Deposit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deposit(self, ctx):
        client = AuthServiceProxy(rpc_connection)
        user_id = str(ctx.author.id)

        if not user_db.check_user(user_id):
            embed = discord.Embed(
                title="**For first-use-user**",
                color=0x0043ff)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="First of all, please type `//help`",
                value="Welcome to world of Tip Sugar !")
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
        else:
            pass

            account = str(ctx.author.id)
            user_name = ctx.author.display_name
            address = client.getaccountaddress(account)

            embed = discord.Embed(
                title="**Your deposit address**",
                color=0x0043ff)
            embed.add_field(
                name="please send sugar to this address.",
                value="Click to enlarge the QR code")
            embed.set_thumbnail(url='https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={0}'.format(address))
            embed.set_author(
                name=user_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
            await ctx.channel.send("```{0}```".format(address))

def setup(bot):
    bot.add_cog(Deposit(bot))