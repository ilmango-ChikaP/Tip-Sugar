from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands

import user_db
import config

# connect to coind
rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

def str_isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class Withdraw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def withdraw(self, ctx, address=None, amount=None):
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

            if address is None or amount is None:
                embed = discord.Embed(color=0xffd800)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="Please check `//help` ",
                    value=" :mag: ")
                embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                 icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                await ctx.channel.send(embed=embed)
            else:
                pass

                if not str_isfloat(amount) or Decimal(amount) < Decimal('0.5'):
                    embed = discord.Embed(color=0xff0000)
                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url_as(format='png', size=256))
                    embed.add_field(
                        name="invalid amount. (amount must be at least 0.5 SUGAR)",
                        value="`{0}`".format(str(amount)))
                    embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                     icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                    await ctx.channel.send(embed=embed)
                else:
                    sendamount = Decimal(str(float(amount))) - \
                                Decimal(str(config.FEE)) # Dealing with cases like "001.100" : "float(amount)"
                    account = str(ctx.author.id)

                    validate = client.validateaddress(address)
                    if not validate['isvalid']:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="invalid address.",
                            value="`{0}`".format(str(address)))
                        embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif Decimal(amount) > client.getbalance(account, config.CONFIRM):
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="You don't have enough balances.",
                            value="Your balances : ```{0} SUGAR```".format(client.getbalance(account, config.CONFIRM)))
                        embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    else:
                        try:
                            txid = client.sendfrom(account, address, float(sendamount))
                        except:
                            embed = discord.Embed(color=0xff0000)
                            embed.set_author(
                                name=ctx.author.display_name,
                                icon_url=ctx.author.avatar_url_as(format='png', size=256))
                            embed.add_field(
                                name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                                value="`{0}`".format(amount))
                            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                            await ctx.channel.send(embed=embed)
                        if len(txid) == 64:
                            tx = client.gettransaction(txid)
                            txfee = tx['fee']
                            client.move(account, "tipsugar_wallet", Decimal(str(config.FEE)))
                            client.move("tipsugar_wallet", account, -txfee)

                            embed = discord.Embed(
                                title="**Block explorer**",
                                url='https://1explorer.sugarchain.org/tx/{0}'.format(txid), color=0x0043ff)
                            embed.set_author(
                                name=ctx.author.display_name,
                                icon_url=ctx.author.avatar_url_as(format='png', size=256))
                            embed.add_field(
                                name="Withdrawal complete `{0} SUGAR`\nwithdraw fee is `{1} SUGAR`\nPlease check the transaction at the above link.".format(sendamount, str(config.FEE)),
                                value="Your balances : `{0} SUGAR`".format(client.getbalance(account, config.CONFIRM)))
                            embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdraw(bot))
