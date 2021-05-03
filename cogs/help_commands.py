import sys
sys.path.append('..')
from botBackend import help_commands
import discord
from discord.ext import commands


class HelpCommands(commands.Cog):

    """This class holds all the commands related to the help commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['help', 'Help'])
    async def help_command(self, ctx, command: str = "default"):

        """displays how to use each command for the bot.
        By default the value is the default help command"""

        # use embed discord styling for nicer display
        embed = discord.Embed(
            title=f"How to use: {command}" if command != "default" else "How to use me",
            description=help_commands.help_draft(command),
            colour=discord.Color.blue()
        )

        # send message as PM
        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
