import discord
from discord.ext import commands
import random
from decouple import config
import sys
sys.path.append('..')

from botBackend.draft_setup_logic import DraftSetupLogic
from botBackend.draft_pick_logic import DraftPickLogic
from botBackend import sheetapi
from botBackend.screenshot import take_screenshot


class DraftSetupPickCommands(commands.Cog):

    """This class holds all the commands related to the draft setup logic
    and draft pick logic commands."""

    def __init__(self, bot):
        self.bot = bot
        self.setup_logic = DraftSetupLogic()
        self.pick_logic = DraftPickLogic()

    @commands.command(aliases=['Cancel', 'cancel'])
    async def cancel_draft(self, ctx):

        """Cancels the current draft during setup."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.cancel_draft(),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Setup', 'setup'])
    async def draft_setup(self, ctx, players: str, picks: str):

        """Sets up the draft with the number
        of players and the number of picks.\n"""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.setup_draft(players, picks),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Edit_player'])
    async def edit_player(self, ctx, player_count: str):

        """Allows the number of players in the draft to be edited."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.edit_player(player_count),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Edit_pick'])
    async def edit_pick(self, ctx, pick_count: str):

        """Allows the number of picks in the draft to be edited."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.edit_pick(pick_count),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Info'])
    async def info(self, ctx):

        """Displays info on the current draft."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.info_draft(),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Join'])
    async def join(self, ctx):

        """Lets a player join the draft provided there is a spot"""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.join_draft(
                                  ctx.message.author.name, ctx.author.mention),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Leave'])
    async def leave(self, ctx):

        """Lets a player leave a draft provided they are in it"""

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(description=self.setup_logic.leave_draft(
                                  ctx.message.author.name, ctx.author.mention),
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Fire', 'fire'])
    async def fire_draft(self, ctx):

        """Fires the draft provided the setup is valid."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):

            # already fired no need to do anything
            if self.setup_logic.draft_fired:
                embed = discord.Embed(description=self.setup_logic.fire_draft(),
                                      colour=discord.Color.blue())
                await ctx.send(embed=embed)

            # otherwise attempt to fire
            else:
                output = self.setup_logic.fire_draft()
                embed = discord.Embed(description=output, colour=discord.Color.blue())
                await ctx.send(embed=embed)

                # if draft does fire successfully
                if self.setup_logic.draft_fired:

                    # shuffle player names and mentions to get an identical random order for draft
                    names_mentions = list(zip(list(self.setup_logic.players.values()),
                                              list(self.setup_logic.players.keys())))
                    random.shuffle(names_mentions)
                    player_names, mentions = zip(*names_mentions)

                    # inform the pick logic that the draft has fired
                    self.pick_logic.fire_draft(list(mentions), self.setup_logic.pick_count)

                    # setup our sheet
                    sheetapi.setupSheet(list(player_names), self.setup_logic.pick_count)

                    # send google doc info
                    link = config('DOCS_LINK')
                    embed = discord.Embed(description=link, colour=discord.Color.blue())
                    embed.set_footer(text=("Setup has been completed. The sheet is available"
                                           "at the link above."))
                    await ctx.send(embed=embed)

                    # notify the first drafter it is their turn to draft
                    await ctx.send(list(mentions)[0] + " it is your turn to pick!")

    @commands.command(aliases=['Pick'])
    async def pick(self, ctx, *card: str):

        """Allows a user to pick a card from the draft.
        The draft needs to have fired for this to work."""

        if not isinstance(ctx.channel, discord.channel.DMChannel):

            # try to make a pick
            username = ctx.message.author.name
            mention = ctx.author.mention
            description = self.pick_logic.pick(username, mention, card)

            # if the draft has been fired and there are no ore picks to make,
            # take a picture then reset it for the next one.
            if self.pick_logic.fired and self.pick_logic.picks_remaining == 0:

                await ctx.send("Draft has been finished. Decks and pictures will arrive shortly.")

                take_screenshot()
                with open('completed_draft.png', 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send(file=picture)

                self.setup_logic.reset()
                self.pick_logic.reset()
                sheetapi.reset_sheet()

            embed = discord.Embed(description=description, colour=discord.Color.blue())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DraftSetupPickCommands(bot))
