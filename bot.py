import discord
import asyncio
import threading
import random
from decouple import config
from discord.ext import commands
from botBackend import scryfallapi
from botBackend.sheetapi import SheetAPI
from botBackend import help_commands
from botBackend import remind
from botBackend.draft_setup_logic import DraftSetupLogic
from botBackend.draft_pick_logic import DraftPickLogic

##########################################
###      BOT SETUP / IMPORT LOGIC      ###
##########################################

# imports to manage the draft.
setup_logic = DraftSetupLogic()
pick_logic = None
sheet_api = None
# initialize bot
bot = commands.Bot(command_prefix="!")
# remove the built in help command so I can write my own
bot.remove_command("help")

##########################################
###             BOT EVENTS             ###
##########################################

@bot.event
async def on_ready():

    """Message the bot sends on startup"""

    print("I am ready to draft! Notify me when you are ready!")

@bot.event
async def on_command_error(ctx, error):
    
    """Handles various errors for user input."""

    if isinstance(error, commands.CommandNotFound): 
        embed = discord.Embed(description = "This command does not exist.", colour = discord.Color.blue())
        await ctx.send(embed = embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description = "Missing required arguments. Use the !help command.", colour = discord.Color.blue())
        await ctx.send(embed = embed)
    else:
        return # silent failure for anything else.

##########################################
###        DRAFT SETUP COMMANDS        ###
##########################################

@bot.command(aliases=['Cancel', 'cancel'])
async def cancel_draft(ctx):

    """Cancels the current draft during setup."""

    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.cancel_draft(), colour = discord.Color.blue())
        await ctx.send(embed = embed)

@bot.command(aliases=['Setup', 'setup'])
async def draft_setup(ctx, players : str, picks : str):

    """Sets up the draft with the number 
    of players and the number of picks.\n"""

    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.setup_draft(players, picks), colour = discord.Color.blue())
        await ctx.send(embed = embed)  
  
@bot.command(aliases=['Edit_player'])
async def edit_player(ctx, player_count : str):
    
    """Allows the number of players in the draft to be edited.""" 

    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.edit_player(player_count), colour = discord.Color.blue())
        await ctx.send(embed = embed)

@bot.command(aliases=['Edit_pick'])
async def edit_pick(ctx, pick_count : str):
    
    """Allows the number of picks in the draft to be edited.""" 
    
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.edit_pick(pick_count), colour = discord.Color.blue())
        await ctx.send(embed = embed)

@bot.command(aliases=['Fire','fire'])
async def fire_draft(ctx):
    
    """This fires the draft provided the setup is valid."""
    
    global pick_logic, sheet_api

    if not isinstance(ctx.channel, discord.channel.DMChannel):

        # see if the draft is already fired
        pre_check = setup_logic.draft_fired

        # attempt to fire
        output = setup_logic.fire_draft()
        embed = discord.Embed(description = output, colour = discord.Color.blue())
        await ctx.send(embed = embed)

        # F -> F will not fire, T -> T means already fired
        # F -> T means we fired and need to call setup
        if pre_check != setup_logic.draft_fired:
            
            # shuffle the player name and mentions to get an identical random order for draft
            names_mentions = list(zip(list(setup_logic.players.values()), list(setup_logic.players.keys()))) 
            random.shuffle(names_mentions) 
            player_names, mentions = zip(*names_mentions) 

            # instantiate our sheet API passing in player names
            sheet_api = SheetAPI(list(player_names), setup_logic.pick_count)
            sheet_api.setupSheet()

            # instantiate pick logic using the mentions
            pick_logic = DraftPickLogic(list(mentions), setup_logic.pick_count)
            
            # send google doc info
            link = config('DOCS_LINK')
            embed = discord.Embed(description = link, colour = discord.Color.blue())
            embed.set_footer(text="Setup has been completed. The sheet is now available at the link above.")
            await ctx.send(embed = embed)
            
            # notify the first drafter it is their turn to draft
            await ctx.send(list(mentions)[0] + " it is your turn to pick!")

@bot.command(aliases=['Info'])
async def info(ctx):

    """this displays info on the current draft."""

    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.info_draft(), colour = discord.Color.blue())
        await ctx.send(embed = embed)

@bot.command(aliases=['Join'])
async def join(ctx):

    """ this lets a player join the draft provided there is a spot"""
    
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.join_draft(ctx.message.author.name, ctx.author.mention), colour = discord.Color.blue())
        await ctx.send(embed = embed)

@bot.command(aliases=['Leave'])
async def leave(ctx):

    """ this lets a player leave a draft provided they are in it""" 
    
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(description = setup_logic.leave_draft(ctx.message.author.name, ctx.author.mention), colour = discord.Color.blue())
        await ctx.send(embed = embed)
 
##########################################
###            HELP COMMANDS           ###
##########################################

@bot.command( pass_context = True, aliases=['help', 'Help'])
async def help_command(ctx, command : str = "default"):

    """displays how to use each command for the bot.
    By default the value is the default help command"""

    # use embed discord styling for nicer display
    embed = discord.Embed(
        title = "How to use: " + command if command != "default" else "How to use me",
        description = help_commands.help_draft(command),
        colour = discord.Color.blue()
    )

    # send message as PM
    await ctx.author.send(embed=embed)

##########################################
###         SCRYFALL COMMANDS          ###
##########################################

@bot.command(aliases=['Card'])
async def card(ctx, *card : str):

    """ returns a card image using scryfall API or notifies card does not exist"""
    try:
        # get the card_url and card_name from the API call
        card_name, image_url = scryfallapi.get_card_image(card)
        embed = discord.Embed(title = card_name, colour = discord.Color.blue())
        embed.set_image(url=image_url)
        await ctx.send(embed = embed)

    except ValueError:
        embed = discord.Embed(description = "This card does not exist.", colour = discord.Color.blue())
        await ctx.send(embed = embed)  
      
@bot.command(aliases=['Legal'])
async def legal(ctx, *card : str):

    """States the legality of a card."""
    try:
        # get the url and card name from the API call
        card_name, legality_json = scryfallapi.get_card_legality(card)
        embed = discord.Embed(title = card_name + " Legality", colour = discord.Color.blue())
        for legality in legality_json:
            embed.add_field(name = "**" + legality + "**", value=legality_json[legality], inline=True)
        await ctx.send(embed = embed)

    except ValueError:
        embed = discord.Embed(description = "This card does not exist.", colour = discord.Color.blue())
        await ctx.send(embed = embed)   
    
##########################################
###           REMIND COMMAND           ###
##########################################

@bot.command(aliases=['Remind', 'remind'])
async def remind_user(ctx, hours : str, minutes : str, seconds : str):
    
    """@'s the caller after a specified amount of time. This can
    be used to remind someone about a pick."""
        
    # valid input
    if remind.valid_time_input(hours, minutes, seconds):  
            
        # setup embed to inform user when they will be notified
        embed = discord.Embed(description = remind.notify(hours, minutes, seconds), colour = discord.Color.blue())
        await ctx.send(embed = embed)

        # send reminder outside of embed so @ works
        await ctx.send(await remind.remind(hours, minutes, seconds, ctx.author.mention))

    else:
        embed = discord.Embed(description = "Invalid parameters. Please use the '!help remind' command for details.", colour = discord.Color.blue())
        await ctx.send(embed = embed)

##########################################
###            PICKS COMMANDS          ###
##########################################

@bot.command(aliases=['Pick'])
async def pick(ctx, *card : str):
    
    global pick_logic, sheet_api

    if pick_logic:        
        username = ctx.message.author.name
        mention = ctx.author.mention
        description = pick_logic.pick(username, mention, card, sheet_api)

        # If the draft is over, reset these for the next one
        if pick_logic.picks_remaining == 0:           
            description = "Congrats! The draft has been finished! Please come and play again sometime."
            setup_logic.reset()
            pick_logic = None
            sheet_api = None
        
        embed = discord.Embed(description = description, colour = discord.Color.blue())
        await ctx.send(embed = embed) 

    else:
        description = "You cannot make picks until the draft has fired."
        embed = discord.Embed(description = description, colour = discord.Color.blue())
        await ctx.send(embed = embed)

##########################################
###             RUN THE BOT            ###
##########################################

def main():
    bot.run(config('BOT_TOKEN'))

if __name__ == "__main__":
    main()
