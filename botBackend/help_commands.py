def help_draft(command : str) -> str:
        
    """displays how to use each command for the bot."""

    fileName = (command + ".txt").lower()

    try: 
        help_text = open("helpCommands/" + fileName, "r")
    
    except FileNotFoundError as e:
        return "No command found."
    
    else:
        help_message = ""
        for line in help_text:
            help_message += line

        help_text.close()
        return help_message
        