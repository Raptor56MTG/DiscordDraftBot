import discord
from discord.ext import commands
import sys
sys.path.append('..')
from botBackend import scryfallapi


class ScryfallCommands(commands.Cog):

    """This class holds all the commands related to the scryfallAPI."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Card'])
    async def card(self, ctx, *card: str):

        """ returns a card image using scryfall API or notifies card does not exist"""
        try:
            # get the card_url and card_name from the API call
            card_name, image_url = scryfallapi.get_card_image(card)
            embed = discord.Embed(title=card_name, colour=discord.Color.blue())
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(description="This card does not exist.",
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(aliases=['Legal'])
    async def legal(self, ctx, *card: str):

        """States the legality of a card."""
        try:
            # get the url and card name from the API call
            card_name, legality_json = scryfallapi.get_card_legality(card)
            embed = discord.Embed(title=f"{card_name} Legality", colour=discord.Color.blue())
            for legality in legality_json:
                embed.add_field(name=f"**{legality}**",
                                value=legality_json[legality],
                                inline=True)
            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(description="This card does not exist.",
                                  colour=discord.Color.blue())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ScryfallCommands(bot))
