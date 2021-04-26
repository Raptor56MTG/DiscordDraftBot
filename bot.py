import discord
from discord.ext import commands
from decouple import config

def main():

    """This is the main method for the bot. It creates the bot,
    and loads in the commands and events from the cogs directory."""

    bot = commands.Bot(command_prefix="!")
    bot.remove_command("help")

    cogs = ['cogs.scryfall_commands', 'cogs.help_commands','cogs.remind_commands',
            'cogs.bot_events', 'cogs.draft_setup_pick_commands', ]
    
    for cog in cogs:
        bot.load_extension(cog)
    
    bot.run(config('BOT_TOKEN'))

if __name__ == "__main__":
    main()
