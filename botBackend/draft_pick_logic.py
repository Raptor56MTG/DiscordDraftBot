from botBackend import scryfallapi
from botBackend import sheetapi


class DraftPickLogic():

    """ this class keeps track of user picks. It stores their picks so that
    they can be called easily without having to open the sheet. It acts as
    the CLI of the draft."""

    def __init__(self):

        # the draft is not fired until we call the fire method
        self.fired = False

        # these are null until the draft has been fired.
        self.players = None
        self.picks_remaining = None
        self.card_tracker = None
        self.row_move = None
        self.column_move = None

        # default starting points for our sheet draft
        self.active_player_index = 0
        self.row = 2
        self.column = 2

    def fire_draft(self, players: list, picks: int):

        """This fires the picks portion of the draft so users
        can start picking cards. It also updates our variables
        to usable values. Note that players is not the players
        names, but their unique user id. This allows the @user
        in discord to be functional and deals with users having
        the same name."""

        # fire the draft
        self.fired = True

        # combine the list + reverse for  [A, B, C] --> [A, B, C, C, B, A]
        self.players = players + players[::-1]
        self.picks_remaining = picks * len(players)
        self.card_tracker = CardTracker(players)

        # list that tells the row and column pointer how to move after every pick.
        self.row_move = ([0] * (len(players) - 1)) + [1] + ([0] * (len(players) - 1)) + [1]
        self.column_move = ([1] * (len(players) - 1)) + [0] + [-1] * ((len(players) - 1)) + [0]

    def reset(self):

        """This resets all values once a draft has finished."""
        self.fired = False
        self.players = None
        self.picks_remaining = None
        self.card_tracker = None
        self.row_move = None
        self.column_move = None

    def pick(self, username: str, mention: str, card: tuple) -> str:

        """This functions as the pipeline for picking occurs.
        All others methods below are executed in series to execute a pick
        in a proper fasion."""

        # make our one off call to scryfall to get the json
        card_json = scryfallapi.get_scryfall_json(card)

        # if input is invalid then break and inform the user
        invalid = self.invalid_input(mention, card_json)
        if invalid:
            return invalid

        # otherwise if valid make the pick
        self.card_tracker.add_card(mention, card_json["name"])
        sheetapi.pick(card_json["name"], self.row, self.column)

        # pipeline to update after pick
        self.row_update()
        self.column_update()
        self.active_player_update()
        self.picks_remaining_update()

        if self.picks_remaining > 0:
            return (f'{username} has chosen {card_json["name"]}. ' +
                    f'{self.players[self.active_player_index]} is up.')
        else:
            return "Congrats! The draft has been finished! Please come and play again sometime."

    ##############################
    ##    PICK PIPELINE BELOW   ##
    ##############################

    def invalid_input(self, mention: str, card_json: dict) -> bool:

        """This checks if the input is invalid."""

        # draft has not been fired
        if not self.fired:
            return "You cannot make picks until the draft has fired."

        # invalid user
        if mention != self.players[self.active_player_index]:
            return "You are not the active drafter. Please wait until it is your turn."

        # card does not exists
        if card_json["object"] == "error":
            return "This card does not exist."

        # get fuzzy corrected name as source of truth and then see that it
        # was already picked.
        if card_json["name"] in self.card_tracker.get_cards():
            return "That card has already been chosen. Please try again."

        return None

    def row_update(self):
        self.row += self.row_move[self.active_player_index]

    def column_update(self):
        self.column += self.column_move[self.active_player_index]

    def active_player_update(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

    def picks_remaining_update(self):
        self.picks_remaining -= 1


class CardTracker():

    """This class acts as the data structure to track
    all of the cards. This is just a dictionary of lists."""

    def __init__(self, players: list):

        self.card_tracker = {}

        for player in players:
            self.card_tracker[player] = []

    def add_card(self, player: str, card_name: str):

        """This adds a card to our dictionary of lists."""

        self.card_tracker[player].append(card_name)

    def get_cards(self) -> list:

        """This gets the list of all of the cards that were chosen."""

        all_picks = []

        for player in self.card_tracker:
            all_picks += self.card_tracker[player]

        return all_picks
