import discord
from discord.ext import commands
from decouple import config
import sys
sys.path.append('..')
from botBackend.draft_logic import DraftLogic
from botBackend.screenshot import take_screenshot


class DraftLogicCommands(commands.Cog):

    """This class holds all the commands related to the draft setup logic
    and draft pick logic commands."""

    def __init__(self, bot):
        self.bot = bot
        self.logic = DraftLogic()

    @commands.command(aliases=['Cancel', 'cancel'])
    async def cancel_draft(self, ctx):

        """Cancels the current draft during setup."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot cancel a draft over DM's."
        else:
            description = self.logic.cancel_draft()

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Setup', 'setup'])
    async def draft_setup(self, ctx, players: str, picks: str):

        """Sets up the draft with the number
        of players and the number of picks."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot setup a draft over DM's."
        else:
            description = self.logic.setup_draft(players, picks)

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Edit_player'])
    async def edit_player(self, ctx, player_count: str):

        """Allows the number of players in the draft to be edited."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot edit a draft over DM's."
        else:
            description = self.logic.edit_player(player_count)

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Edit_pick'])
    async def edit_pick(self, ctx, pick_count: str):

        """Allows the number of picks in the draft to be edited."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot edit a draft over DM's."
        else:
            description = self.logic.edit_pick(pick_count)

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Info'])
    async def info(self, ctx):

        """Displays info on the current draft."""
        embed = discord.Embed(description=self.logic.info_draft(), colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Join'])
    async def join(self, ctx):

        """Lets a player join the draft provided there is a spot"""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot join a draft over DM's."
        else:
            description = self.logic.join_draft(ctx.message.author.name, ctx.author.id)

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Leave'])
    async def leave(self, ctx):

        """Lets a player leave a draft provided they are in it"""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot leave a draft over DM's."
        else:
            description = self.logic.leave_draft(ctx.message.author.name, ctx.author.id)

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Fire', 'fire'])
    async def fire_draft(self, ctx):

        """Fires the draft provided the setup is valid."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = "Cannot fire a draft over DM's."
        else:
            await ctx.send("Attempting to fire the draft. Please wait a moment.")
            description = self.logic.fire_draft()

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Pick', 'P', 'p'])
    async def pick(self, ctx, *card: str):

        """Allows a user to pick a card from the draft.
        The draft needs to have fired for this to work."""
        
        # get the id of the channel we want to send to
        channel = self.bot.get_channel(config('CHANNEL_ID'))

        # try to make the pick
        embed = discord.Embed(description=self.logic.pick(
                              ctx.message.author.name, ctx.author.id, card),
                              colour=discord.Color.blue())
        await channel.send(embed=embed)

        # if we have reached the end of the draft.
        if self.logic.picks_remaining == 0 and self.logic.draft_fired:

            # send deck files
            await self.generate_text_files(ctx)

            # take a screenshot
            take_screenshot()
            with open('completed_draft.png', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            # reset logic for next draft
            self.logic.reset()
            await channel.send("Thank you all for playing! Come back soon.")

    @commands.command(aliases=['Pre_pick', 'Prepick', 'prepick', 'Pp', 'pp'])
    async def pre_pick(self, ctx, *card: str):

        """Allows users to make pre-picks in the draft."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = self.logic.pre_pick(ctx.message.author.name, ctx.author.id, card)
        else:
            description = "Please send pre-picks over DM's."

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Cancel_pre_pick',
                               'Cancelprepick', 'cancelprepick',
                               'Cancel_prepick', 'cancel_prepick',
                               'Cpp', 'cpp'])
    async def cancel_pre_pick(self, ctx, *card: str):

        """Allows users to cancel pre-picks in the draft."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = self.logic.cancel_pre_pick(ctx.message.author.name, ctx.author.id, card)
        else:
            description = "Please cancel pre-picks over DM's."

        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Get_pre_picks',
                               'Get_prepicks', 'get_prepicks',
                               'Getprepicks', 'getprepicks',
                               'Gpp', 'gpp'])
    async def get_pre_picks(self, ctx):

        """Allows a user to see their prepicks in the draft."""

        if isinstance(ctx.channel, discord.channel.DMChannel):
            description = self.logic.get_pre_picks(ctx.message.author.name, ctx.author.id)
        else:
            description = "Please cancel pre-picks over DM's."
        
        embed = discord.Embed(description=description, colour=discord.Color.blue())
        await ctx.send(embed=embed)

    ############################
    ###   HELPER FUNCTIONS   ###
    ############################

    async def generate_text_files(self, ctx):

        """This generates the text file for the users. I am not a fan
        of having this logic outside of the  pick logic, but it is what
        it is."""

        for player in self.logic.picks:

            # populate the text file with their deck
            with open("deck.txt", "w") as file:
                for card in self.logic.picks[player]:
                    file.write(f"1 {card}\n")

            # send them their text file
            with open("deck.txt", "rb") as file:
                await ctx.send(f"{player.username}'s deck",
                               file=discord.File(file, "rotisserie_deck.txt"))

            # clear the text file so we can refill it with the next deck.
            with open('deck.txt', 'w'):
                pass


def setup(bot):
    bot.add_cog(DraftLogicCommands(bot))
