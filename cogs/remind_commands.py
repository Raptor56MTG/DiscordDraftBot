import discord
from discord.ext import commands
import sys
sys.path.append('..')
from botBackend import remind


class RemindCommands(commands.Cog):

    """This class holds all the commands related to the remind commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Remind', 'remind'])
    async def remind_user(self, ctx, hours: str, minutes: str, seconds: str):

        """@'s the caller after a specified amount of time. This can
        be used to remind someone about a pick."""

        # valid input
        if remind.valid_time_input(hours, minutes, seconds):

            # setup embed to inform user when they will be notified
            embed = discord.Embed(description=remind.notify(hours, minutes, seconds),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

            # send reminder outside of embed so @ works
            await ctx.send(await remind.remind(hours, minutes, seconds, ctx.author.mention))

        else:
            embed = discord.Embed(
                description="Invalid parameters. Use the '!help remind' command for details.",
                colour=discord.Color.blue())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RemindCommands(bot))
