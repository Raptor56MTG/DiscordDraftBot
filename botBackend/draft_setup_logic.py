class DraftSetupLogic():

    """This class holds the setup drafting logic
    for the bot. This includes joining, leaving,
    and setting up attributes of the draft."""

    def __init__(self):

        # constants for bounds
        self.PLAYER_COUNT_MIN = 1
        self.PLAYER_COUNT_MAX = 8
        self.PICK_COUNT_MIN = 5
        self.PICK_COUNT_MAX = 100

        # attributes of draft
        self.player_count = 0
        self.pick_count = 0
        self.players = {}

        # determines if the draft is in the process of being set up
        self.setup = False

        # once fired, setup cannot be modified.
        self.draft_fired = False

    def cancel_draft(self) -> str:

        """This cancels a draft if it has not fired, and no
        one has joined it."""

        if not self.setup:
            return "You cannot cancel a draft that was not set up."

        elif self.draft_fired:
            return "You cannot cancel a draft that has fired."

        elif len(self.players) > 0:
            return "All players must leave the draft for it to be cancelled."

        else:
            self.setup = False
            return "The draft setup has been cancelled."

    def info_draft(self) -> str:

        """this displays info on the current draft"""

        if not self.setup:
            return "The draft has not been set up."
        else:
            info = (f"```player_count is: {self.player_count}\n" +
                    f"pick_count is: {self.pick_count}\n" +
                    f"draft_fired status is: {self.draft_fired}\n" +
                    "Current joined drafters are:\n")

            for drafter in self.players:
                info += f"{self.players[drafter]}\n"

            info += "```"
            return info

    def fire_draft(self) -> str:

        """This fires the draft provided parameters are correct.
        Once the draft fires the setup cannot be altered."""

        if self.draft_fired:
            return "The draft has already fired."

        elif not self.setup:
            return "The draft has not been set up."

        elif len(self.players) != self.player_count:
            return "Please ensure that the draft is full."
        else:
            self.draft_fired = True
            return ("The draft has fired and is currently being set up. " +
                    "All other commands are disabled until sheet setup is complete.")

    def join_draft(self, username: str, mention: str) -> str:

        """ this lets a player join the draft provided there is a spot"""

        if self.draft_fired:
            return "The draft has already fired and cannot be joined."

        elif not self.setup:
            return "The draft has not been set up."

        elif mention in self.players:
            return f"{username} has already been added to the draft."

        elif len(self.players) < self.player_count:
            self.players[mention] = username
            return f"{username} has been added to the draft."
        else:
            return "The draft is full. Please join the next draft!"

    def leave_draft(self, username: str, mention: str) -> str:

        """ this lets a player leave a draft provided they are in it"""

        if self.draft_fired:
            return "The draft has already fired and must be finished."

        elif mention in self.players:
            del self.players[mention]
            return f"{username} has left the draft."
        else:
            return "You cannot leave the draft if you never joined."

    def setup_draft(self, player_count: str, pick_count: str) -> str:

        """Sets up the draft with the number of players and
        the number of picks."""

        if self.draft_fired:
            return ("The draft has already fired. Please wait for it to be " +
                    "finished before starting another draft.")

        elif self.setup:
            return ("The draft setup has already been completed. " +
                    "To modify the setup use the edit commands.")

        # Invalid input (invalid value, or out of bounds)
        elif (not pick_count.isdigit() or not player_count.isdigit() or
              int(pick_count) < self.PICK_COUNT_MIN or int(player_count) < self.PLAYER_COUNT_MIN or
              int(pick_count) > self.PICK_COUNT_MAX or int(player_count) > self.PLAYER_COUNT_MAX):
            return "Invalid parameters. Please use the '!help setup' command for details."

        else:
            self.player_count = int(player_count)
            self.pick_count = int(pick_count)
            self.setup = True
            return (f"The draft has been set up. We have {self.player_count} players and " +
                    f"{self.pick_count} picks. Use the !join command to be added to the draft.")

    def edit_player(self, player_count: str) -> str:

        """Allows for the player count to be edited during draft setup."""

        if self.draft_fired:
            return "The draft has already fired. It cannot be edited."

        elif not self.setup:
            return "The draft has not been set up. It cannot be edited."

        # invalid input (not a number, or out of bounds)
        elif (not player_count.isdigit() or int(player_count) < self.PLAYER_COUNT_MIN
              or int(player_count) > self.PLAYER_COUNT_MAX):
            return "Invalid parameters. Please use the '!help edit_player' command for details."

        # input is smaller than the current number of players enrolled
        elif len(self.players) > int(player_count):
            return ("The draft currently has too many players to go to " + player_count +
                    " players. Please have players leave before making the edit.")

        else:
            self.player_count = int(player_count)
            return "Player count is: " + str(self.player_count)

    def edit_pick(self, pick_count: str) -> str:

        """Allows for the pick count to be edited during draft setup."""

        if self.draft_fired:
            return "The draft has already fired. It cannot be edited."

        elif not self.setup:
            return "The draft has not been set up. It cannot be edited."

        # if invalid input (not a number, or out of bounds)
        elif (not pick_count.isdigit() or int(pick_count) < self.PICK_COUNT_MIN
              or int(pick_count) > self.PICK_COUNT_MAX):
            return "Invalid parameters. Please use the '!help edit_pick' command for details."

        else:
            self.pick_count = int(pick_count)
            return "Pick count is: " + str(self.pick_count)

    def reset(self):

        """Resets the class values back to default
        once the draft has been finished."""

        # reset back to defaults
        self.player_count = 0
        self.pick_count = 0
        self.players = {}
        self.setup = False
        self.draft_fired = False
