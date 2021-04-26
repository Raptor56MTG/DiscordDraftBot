def help_draft(command : str) -> str:
        
    """displays how to use each command for the bot."""

    try:
        fileName = command.lower() + ".txt" 
       
        help_message = ""
        with open("helpCommands/" + fileName, "r") as help_text: 
            for line in help_text:
                help_message += line

        return help_message

    except FileNotFoundError:
        return "No command found."
            