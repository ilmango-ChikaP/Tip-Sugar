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

class Tip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tip(self, ctx, mention=None, amount=None):
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

            if mention is None or amount is None:
                embed = discord.Embed(color=0xffd800)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="Please check `//help` ",
                    value=" :mag: ")
                embed.set_footer(
                    text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                    icon_url=self.bot.user.avatar_url_as(format='png', size=256))
                await ctx.channel.send(embed=embed)
            elif not str_isfloat(amount):
                embed = discord.Embed(color=0xff0000)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="invalid amount.",
                    value="`{0}`".format(amount))
                embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                 icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                await ctx.channel.send(embed=embed)
            else:
                pass

                tipfrom = str(ctx.author.id)
                tipto = str(mention.replace('<@','').replace('>',''))
                amount = Decimal(str(float(amount))) # Dealing with cases like "001.100", ".123" : "float(amount)"

                if amount < Decimal('0.00000001'):
                    embed = discord.Embed(color=0xff0000)
                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url_as(format='png', size=256))
                    embed.add_field(
                        name="amount must be at least 0.00000001 SUGAR",
                        value="`{0}`".format(amount))
                    embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                     icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                    await ctx.channel.send(embed=embed)
                else:
                    if len(tipto) != 18 and len(tipto) != 17: # length of discord user id is 18 or 17
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="invalid user.",
                            value="`{0}`".format(str(mention)))
                        embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif tipfrom == tipto:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="You cannot tip to yourself.",
                            value=" :thinking: ")
                        embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif amount > client.getbalance(tipfrom, config.CONFIRM):
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="You don't have enough balances.",
                            value="Your balances ```{0} SUGAR```".format(client.getbalance(tipfrom, config.CONFIRM)))
                        embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    else:
                        if tipto == str(self.bot.user.id):
                            try:
                                move_istrue = client.move(tipfrom, 'tipsugar_wallet', float(amount))
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
                            if move_istrue:
                                embed = discord.Embed(color=0x0043ff)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="Thank you for donating!",
                                    value="```{0} SUGAR```".format(amount))
                                embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                                 icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)
                        else:
                            try:
                                move_istrue = client.move(tipfrom, tipto, float(amount))
                            except:
                                embed = discord.Embed(color=0xff0000)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                                    value="`{0}`".format(amount))
                                embed.set_footer(
                                    text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                    icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)
                            if move_istrue:
                                embed = discord.Embed(color=0x0043ff)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="{0} tipped to {1} `{2} SUGAR`".format(ctx.author.display_name,
                                                                                self.bot.get_user(int(tipto)).display_name,
                                                                                amount),
                                    value="yay!")
                                embed.set_footer(text="Tip Sugar {0} [Owner: {1}]".format(config.VERSION, self.bot.get_user(config.OWNER_ID)),
                                                 icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Tip(bot))