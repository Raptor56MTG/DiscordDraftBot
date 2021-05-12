from dataclasses import dataclass
from decouple import config
import random
from botBackend import scryfallapi
from botBackend import sheetapi


@dataclass(frozen=True)
class Player():

    """This is the data class for the Player.
    Contains their username, and their unique user id."""

    username: str
    user_id: str


class DraftLogic():

    """This class holds the setup drafting logic
    for the bot. This includes joining, leaving,
    and setting up attributes of the draft."""

    def __init__(self):

        # constants for setup bounds
        self.PLAYER_COUNT_MIN = 1
        self.PLAYER_COUNT_MAX = 8
        self.PICK_COUNT_MIN = 5
        self.PICK_COUNT_MAX = 100

        # setup values 
        self.player_count = 0
        self.pick_count = 0
        self.players = []
        self.picks = {}
        self.setup = False
        self.draft_fired = False

        # pick values and info to inform the google
        # sheet api where to move.
        self.active_player_index = 0
        self.row = 2
        self.column = 2
        self.snake_player_list = None
        self.row_move = None
        self.column_move = None
        self.picks_remaining = None

    ###################################
    ###      DRAFT SETUP LOGIC      ###
    ###################################

    def cancel_draft(self) -> str:

        """This cancels a draft if it has not fired, and no
        one has joined it."""

        if self.draft_fired:
            return "You cannot cancel a draft that has fired."

        elif not self.setup:
            return "You cannot cancel a draft that's not set up."

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

            for player in self.players:
                info += f"{player.username}\n"

            info += "```"
            return info

    def join_draft(self, username: str, user_id: str) -> str:

        """ this lets a player join the draft provided there is a spot"""

        if self.draft_fired:
            return "The draft has already fired and cannot be joined."

        elif not self.setup:
            return "The draft has not been set up."

        elif Player(username, user_id) in self.players:
            return f"{username} has already been added to the draft."

        elif len(self.players) < self.player_count:
            self.players.append(Player(username, user_id))
            self.picks[Player(username, user_id)] = []
            return f"{username} has been added to the draft."
        else:
            return "The draft is full. Please join the next draft!"

    def leave_draft(self, username: str, user_id: str) -> str:

        """ this lets a player leave a draft provided they are in it"""

        if self.draft_fired:
            return "The draft has already fired and must be finished."

        elif Player(username, user_id) in self.players:
            self.players.remove(Player(username, user_id))
            del self.picks[Player(username, user_id)]
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

    ###################################
    ###       DRAFT PICK LOGIC      ###
    ###################################

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
            # fire the draft 
            self.draft_fired = True

            # shuffle the player order to randomize it
            random.shuffle(self.players)

            # assign the snake order for the rotissare draft [A, B, C, C, B, A]
            self.snake_player_list = self.players + self.players[::-1]

            # use this to determine how many picks we have remaining
            self.picks_remaining = self.pick_count * self.player_count

            # instantiate the lists to inform the google sheet API how to move
            self.row_move = ([0] * (self.player_count - 1)) + [1] + ([0] * (self.player_count - 1)) + [1]
            self.column_move = ([1] * (self.player_count - 1)) + [0] + [-1] * ((self.player_count - 1)) + [0]

            # append usernames to sheet
            player_names = [player.username for player in self.players]
            sheetapi.setup_sheet(player_names, self.pick_count)

            return (f"Setup has been completed.\n\nSheet is available here: {config('DOCS_LINK')}\n\n" + 
                    f"{self.snake_player_list[0].user_id} is up first.")

    def pick(self, username: str, user_id: str, card: tuple) -> str:

        """This functions as the pipeline for picking occurs.
        All others methods below are executed in series to execute a pick
        in a proper fasion."""

        # make 1 time call to scryfall
        card_json = scryfallapi.get_scryfall_json(card)

        # check if input is not valid
        invalid = self.invalid_pick(username, user_id, card_json)
        if invalid:
            return invalid

        # otherwise if valid make the pick and add to sheet
        self.picks[Player(username, user_id)].append(card_json["name"])
        sheetapi.pick(card_json["name"], self.row, self.column)

        # pipeline to update after pick
        self.row_update()
        self.column_update()
        self.active_player_update()
        self.picks_remaining_update()

        if self.picks_remaining > 0:
            return (f'{username} has chosen {card_json["name"]}. ' +
                    f'{self.snake_player_list[self.active_player_index].user_id} is up.')
        else:
            return "Congrats! The draft has been finished! Decks and pictures will arrive shortly."

    def invalid_pick(self, username: str, user_id: str, card_json: dict):

        """Determines if a pick was invalid."""

        if not self.draft_fired:
            return "You cannot make picks until the draft has fired."

        if Player(username, user_id) != self.snake_player_list[self.active_player_index]:
            return "You are not the active drafter. Please wait until it is your turn."

        if card_json["object"] == "error":
            return "This card does not exist."

        # used list comprehension here to combine all the lists
        # in the dictionary into one list that can be searched.
        if card_json["name"] in [cards for picks in self.picks.values() for cards in picks]:
            return "That card has already been chosen. Please try again."

        return None

    def row_update(self):
        self.row += self.row_move[self.active_player_index]

    def column_update(self):
        self.column += self.column_move[self.active_player_index]

    def active_player_update(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.snake_player_list)

    def picks_remaining_update(self):
        self.picks_remaining -= 1

    ###################################
    ###      RESET DRAFT LOGIC      ###
    ###################################

    def reset(self):

        """Resets the class values back to default
        once the draft has been finished."""

        # reset setup values back to defaults
        self.player_count = 0
        self.pick_count = 0
        self.players = []
        self.draft_fired = False
        self.setup = False

        # reset pick / sheet api values to defaults
        self.picks = {}
        self.active_player_index = 0
        self.snake_player_list = None
        self.row = 2
        self.column = 2
        self.row_move = None
        self.column_move = None
        self.picks_remaining = None

        # call sheet api to reset
        sheetapi.reset_sheet()
