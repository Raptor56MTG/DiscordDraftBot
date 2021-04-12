# DiscordDraftBotRepo

This is the code for the DraftBot Discord Bot used to play Rotissare Drafts.

# Installation and Setup

1. Clone the repository to your local machine.
2. Run pipenv shell to create a environent that can run the code.
3. You will need to create a credentials file for the google sheets API.
   A good tutorial on this topic can be seen here: https://www.youtube.com/watch?v=cnPlKLEGR7E. 
   
   Keep in mind that these credentials should be treated as secrets. An example of what
   this should look like is the example_credentials.txt file. This is a placeholder and
   can be deleted once you have your actual credentials file.
   
4. Set up your discord bot and discord bot token. The bot token should not
   be published and should be stored in your environment variables. An example of what
   this should look like is the example_env.txt file. This is a placeholder and
   can be deleted once you have your actual environment variables set.
   
5. Run bot.py and enjoy.

# Testing

If you want to test the code, use 'python -m unittest'.



