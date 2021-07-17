def help_draft(command: str) -> str:

    """displays how to use each command for the bot."""

    try:
        fileName = f"{command.lower()}.txt"

        with open(f"helpCommands/{fileName}", "r") as f:
            help_message = ''.join(f.readlines())

        return help_message

    except FileNotFoundError:
        return "No command found."
