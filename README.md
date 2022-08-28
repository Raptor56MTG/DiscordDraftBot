# DiscordDraftBotRepo

This is the code for the DraftBot Discord Bot used to play Rotissare Drafts.

## Important Information / Common questions

### What does this bot do?

   The goal of this bot is to fully automate a rotisserie draft. This includes
   picking cards, generating decklists, and taking a screenshot of the finished
   draft.

### Can this bot run in multiple servers at the same time?
   Unfourtunatly it cannot. This bot is intended to be run in one server only. This is due to the limitations that come with accessing a google sheet. If you want this bot to run in multiple servers, you will need to create a new bot instance and credentials for each server.
   
## Possible hiccups / Things to keep in mind during setup

- dependencies and environment are both handled with pipenv.
- You can host this anywhere, but I will specify how to set this up on Heroku.
- I have included some example txt files as placeholders for credentials, links, and keys. These will help you ensure you have everything you need and should be deleted later on.
- Make sure that keys, tokens, credentials, links, and other secrets do not get published or posted in the wrong places! Store them as secrets in a secure manner. I have placeholders for these in the example text files. These can be used to help ensure you have all the needed credentials, and can be deleted afterwards.

## Setup steps

1. Clone the repository to your local machine. If you want to run it locally, run 'pipenv install' to create the environment and dependencies.

2. Set up a discord bot usng the discord API. You can visit the Discord developer portal for more information, as well as watch various tutorials on youtube and elsewhere to show how to set this up. Developer Portal link: https://discord.com/developers/docs/intro
   
3. You will need to create a credentials file for the google sheets API. A good tutorial on this topic can be seen here: https://www.youtube.com/watch?v=cnPlKLEGR7E. 
    
4. If you plan on running this code locally before hosting it, download chromedriver for selenium to allow the screenshot code to function properly. This should be stored in the main project directory. If you plan on hosting this on Heroku the chromedriver executable is not required and a buildpack should be used.

5. Create an account on Heroku for hosting. A good tutorial on how to create a Heroku account for a discord bot can be seen here: https://www.youtube.com/watch?v=BPvg9bndP1U 

6. Addressing hiccups that you might encounter while setting up your bot on Heroku

   - How do I securely store the json credentials file? 
      - I found the following tutorial helpful in this endeavor: https://dev.to/sylviapap/setting-heroku-config-vars-with-google-cloud-json-file-on-rails-4dnf 

   - How do I get chromedriver working on heroku?
      - I found the following tutorial helpful in this endeavor: https://www.youtube.com/watch?v=Ven-pqwk3ec

7. Once you have your bot hosted, you should be ready to go. If you want to run it locally, just use the command 'python bot.py'.

# Styling/Linting

I use flake8 to help enforce PEP8 rules.

# Testing

If you want to test the code, use 'python -m unittest'.

This repo uses basic Github CI for pull requests via flake8 and unit tests.
