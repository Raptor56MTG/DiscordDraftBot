from dataclasses import dataclass
from decouple import config
import random
import json
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

        # list of legal formats users can play in
        self.FORMATS = ["standard", "future", "historic", "gladiator",
                        "pioneer", "modern", "legacy", "pauper",
                        "vintage", "penny", "commander", "brawl",
                        "duel", "oldschool", "premodern", "freeform"]

        # setup values back to defaults
        self.player_count = 0
        self.pick_count = 0
        self.players = []
        self.draft_fired = False
        self.setup = False
        self.format = None

        # pick values and info to inform the google
        # sheet api where to move.
        self.picks = {}
        self.prepicks = {}
        self.active_player_index = 0
        self.row = 2
        self.column = 2
        self.row_move = []
        self.column_move = []
        self.picks_remaining = 0
        self.snake_player_list = []

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
                    f"format is: {self.format}\n" +
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
            self.prepicks[Player(username, user_id)] = []
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
            del self.prepicks[Player(username, user_id)]
            return f"{username} has left the draft."
        else:
            return "You cannot leave the draft if you never joined."

    def setup_draft(self, player_count: str, pick_count: str, format: str) -> str:

        """Sets up the draft with the number of players and
        the number of picks."""

        if self.draft_fired:
            return ("The draft has already fired. Please wait for it to be " +
                    "finished before starting another draft.")

        elif self.setup:
            return ("The draft setup has already been completed. " +
                    "To modify the setup use the edit commands.")

        # Invalid input (invalid value, or out of bounds)
        elif (format.lower() not in self.FORMATS or
              not pick_count.isdigit() or not player_count.isdigit() or
              int(pick_count) < self.PICK_COUNT_MIN or int(player_count) < self.PLAYER_COUNT_MIN or
              int(pick_count) > self.PICK_COUNT_MAX or int(player_count) > self.PLAYER_COUNT_MAX):
            return "Invalid parameters. Please use the '!help setup' command for details."

        else:
            self.player_count = int(player_count)
            self.pick_count = int(pick_count)
            self.setup = True
            self.format = format
            return (f"The draft has been set up. We have {self.player_count} players, " +
                    f"{self.pick_count} picks, and the format is {self.format}. " +
                    "Use the !join command to be added to the draft.")

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
            return f"Player count is: {self.player_count}"

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
            return f"Pick count is: {self.pick_count}"

    def edit_format(self, format: str) -> str:

        """Allows for the format to be edited during draft setup."""

        if self.draft_fired:
            return "The draft has already fired. It cannot be edited."

        elif not self.setup:
            return "The draft has not been set up. It cannot be edited."

        # if invalid input (not a number, or out of bounds)
        elif (format.lower() not in self.FORMATS):
            return "Invalid parameters. Please use the '!help edit_format' command for details."
        else:
            self.format = format.lower()
            return f"Format is: {self.format}"

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
            self.row_move = (([0] * (self.player_count - 1)) + [1] +
                             ([0] * (self.player_count - 1)) + [1])
            self.column_move = (([1] * (self.player_count - 1)) + [0] +
                                [-1] * ((self.player_count - 1)) + [0])

            # append usernames to sheet
            player_names = [player.username for player in self.players]
            sheetapi.setup_sheet(player_names, self.pick_count)

            # backup the state of the draft
            self.backup()

            return ("Setup has been completed.\n\nSheet is available here: " +
                    f"{config('DOCS_LINK')}\n\n" +
                    f"{self.snake_player_list[0].username} is up first.")

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
        self.prepicks_update(card_json["name"])

        # see if there are any prepicks that can be made
        pre_picks_made = self.iterate_prepicks()

        # backup the state of the draft
        self.backup()

        # informs us about the picks and prepicks made
        statement = ""
        statement += f"{username} has chosen {card_json['name']}.\n"
        for pre_pick in pre_picks_made:
            statement += f"{pre_pick[0]} has chosen {pre_pick[1]}.\n"

        if self.picks_remaining > 0:
            statement += f"{self.snake_player_list[self.active_player_index].username} is up."
        else:
            statement += ("Congrats! The draft has been finished! " +
                          "Decks and pictures will arrive shortly.")

        return statement

    def iterate_prepicks(self):

        """This iterates through the prepicks until the active player
        has no prepicks to make, or the draft is over."""

        more_prepicks = True
        more_picks = self.picks_remaining > 0

        total_picks = []

        while more_prepicks and more_picks:

            # get the new active player
            active_player = self.snake_player_list[self.active_player_index]

            # if they have no picks to make, we are done
            if not self.prepicks[active_player]:
                more_prepicks = False

            else:
                # make the pick for that player
                pick = self.prepicks[active_player].pop(0)
                self.picks[active_player].append(pick)
                sheetapi.pick(pick, self.row, self.column)

                # pipeline to update after pick
                self.row_update()
                self.column_update()
                self.active_player_update()
                self.picks_remaining_update()
                self.prepicks_update(pick)

                # append the total picks so we know who did what.
                total_picks.append((active_player.username, pick))

                # ensure we have more picks to make
                more_picks = self.picks_remaining > 0

        return total_picks

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

        if (self.format != "freeform" and (card_json["legalities"][self.format] == "banned" or
           card_json["legalities"][self.format] == "not_legal")):
            return f"This card is not legal in {self.format}."

        return None

    ###################################
    ###    PICK UPDATE PIPELINE     ###
    ###################################

    def row_update(self):
        self.row += self.row_move[self.active_player_index]

    def column_update(self):
        self.column += self.column_move[self.active_player_index]

    def active_player_update(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.snake_player_list)

    def picks_remaining_update(self):
        self.picks_remaining -= 1

    def prepicks_update(self, card: str):

        """This goes through the prepicks, and it removes
        any prepicks that match the pick that was just made.
        This will ensure that there are no redundant picks made."""

        # iterate through all of the players
        for player in self.prepicks:

            # if the most recent pick is in their prepicks, remove it
            if card in self.prepicks[player]:
                self.prepicks[player].remove(card)

    ###################################
    ###    DRAFT PRE-PICK LOGIC     ###
    ###################################

    def pre_pick(self, username: str, user_id: str, card: tuple) -> str:

        """"Allows users to pick cards in advance."""

        # make 1 time call to scryfall
        card_json = scryfallapi.get_scryfall_json(card)

        # check if input is not valid
        invalid = self.invalid_prepick(username, user_id, card_json)
        if invalid:
            return invalid

        # otherwise if valid make the pre pick
        self.prepicks[Player(username, user_id)].append(card_json["name"])

        # backup the prepick list
        self.backup()

        return f"You have successfully pre-picked: {card_json['name']}."

    def cancel_pre_pick(self, username: str, user_id: str, card: tuple) -> str:

        """"Allows users to cancel prepicks."""

        # make 1 time call to scryfall
        card_json = scryfallapi.get_scryfall_json(card)

        # check if input is not valid
        invalid = self.invalid_cancel_prepick(username, user_id, card_json)
        if invalid:
            return invalid

        # otherwise remove prepick
        self.prepicks[Player(username, user_id)].remove(card_json["name"])

        # backup the prepick list
        self.backup()

        return f"You have successfully removed: {card_json['name']}."

    def get_pre_picks(self, username, user_id) -> str:

        if not self.draft_fired:
            return "No pre-picks as draft has not fired."

        if Player(username, user_id) not in self.prepicks:
            return "You are not in this draft and have no pre-picks."

        if len(self.prepicks[Player(username, user_id)]) == 0:
            return "Pre-pick queue is empty."

        prepicks = "```"

        for i, prepick in enumerate(self.prepicks[Player(username, user_id)], start=1):
            prepicks += f"{i}. {prepick}\n"

        prepicks += "```"

        return prepicks

    def invalid_cancel_prepick(self, username: str, user_id: str, card_json: dict) -> str:

        """Determines if a cancelled pre-pick was invalid."""

        if not self.draft_fired:
            return "You cannot cancel pre-picks until the draft has fired."

        if Player(username, user_id) not in self.prepicks:
            return "You are not in this draft and cannot cancel pre-picks."

        if card_json["object"] == "error":
            return "This card does not exist."

        if card_json["name"] not in self.prepicks[Player(username, user_id)]:
            return "Cannot remove cards you have not pre-picked."

        return None

    def invalid_prepick(self, username: str, user_id: str, card_json: dict) -> str:

        """Determines if a pre-pick was invalid."""

        if not self.draft_fired:
            return "You cannot make pre-picks until the draft has fired."

        if Player(username, user_id) not in self.prepicks:
            return "You are not in this draft and cannot make pre-picks."

        if card_json["object"] == "error":
            return "This card does not exist."

        if (self.format != "freeform" and (card_json["legalities"][self.format] == "banned" or
           card_json["legalities"][self.format] == "not_legal")):
            return f"This card is not legal in {self.format}."

        # used list comprehension here to combine all the lists
        # in the dictionary into one list that can be searched.
        if card_json["name"] in [cards for picks in self.picks.values() for cards in picks]:
            return "That card has already been chosen in the draft. Please try again."

        if card_json["name"] in self.prepicks[Player(username, user_id)]:
            return "You have already pre-picked this card. Please try again."

        return None

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
        self.format = None

        # reset pick / sheet api values to defaults
        self.picks = {}
        self.prepicks = {}
        self.active_player_index = 0
        self.row = 2
        self.column = 2
        self.row_move = []
        self.column_move = []
        self.picks_remaining = 0
        self.snake_player_list = []

        # backup the state of the draft to being reset
        self.backup()

        # call sheet api to reset
        sheetapi.reset_sheet()

    ###################################
    ###      BACKUP DRAFT LOGIC     ###
    ###################################

    def backup(self):
        """This stores all values in cache into a backup
        json file to cover the case where the bot crashes.
        This ensures the bot can be reloaded and the draft
        can pick up from where it left off. I will note
        that this is a bit yucky / manual due to dataclasses
        not being jsonable. As a result, I have to manual this a bit."""

        with open("storage.json", "r") as file:
            data = json.load(file)
        data["player_count"] = self.player_count
        data["pick_count"] = self.pick_count
        data["players"] = [{"username": player.username,
                            "user_id": player.user_id}
                           for player in self.players]
        data["draft_fired"] = self.draft_fired
        data["setup"] = self.setup
        data["format"] = self.format
        data["picks"] = [{"username": player.username,
                          "user_id": player.user_id,
                          "picks": self.picks[player]}
                         for player in self.picks]
        data["prepicks"] = [{"username": player.username,
                             "user_id": player.user_id,
                             "prepicks": self.prepicks[player]}
                            for player in self.prepicks]
        data["active_player_index"] = self.active_player_index
        data["row"] = self.row
        data["column"] = self.column
        data["row_move"] = self.row_move
        data["column_move"] = self.column_move
        data["picks_remaining"] = self.picks_remaining
        data["snake_player_list"] = [{"username": player.username,
                                      "user_id": player.user_id}
                                     for player in self.snake_player_list]

        with open("storage.json", "w") as file:
            json.dump(data, file)

    def reload(self):
        """This loads in stored data from a json file to
        restore a draft to a previous stage."""

        with open("storage.json", "r") as file:
            data = json.load(file)
        self.player_count = data["player_count"]
        self.pick_count = data["pick_count"]
        self.players = [Player(player["username"], player["user_id"]) for player in data["players"]]
        self.draft_fired = data["draft_fired"]
        self.setup = data["setup"]
        self.format = data["format"]

        self.picks = {Player(player["username"], player["user_id"]): player["picks"]
                      for player in data["picks"]}
        self.prepicks = {Player(player["username"], player["user_id"]): player["prepicks"]
                         for player in data["prepicks"]}
        self.active_player_index = data["active_player_index"]
        self.row = data["row"]
        self.column = data["column"]
        self.row_move = data["row_move"]
        self.column_move = data["column_move"]
        self.picks_remaining = data["picks_remaining"]
        self.snake_player_list = [Player(player["username"], player["user_id"])
                                  for player in data["snake_player_list"]]
