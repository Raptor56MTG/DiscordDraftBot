import gspread
from botBackend import scryfallapi 
from botBackend import sheetapi

class DraftPickLogic():

    """ this class keeps track of user picks. It stores their picks so that 
    they can be called easily without having to open the sheet. It acts as 
    the CLI of the draft."""

    def __init__(self, players : list, picks : int):

        # combine the list + reverse for  [A, B, C] --> [A, B, C, C, B, A]
        self.players = players + players[::-1]
        self.active_player_index = 0
        self.picks_remaining = picks * len(players)
        self.card_tracker = CardTracker(players)

        # starting points for our sheet draft
        self.row = 2
        self.column = 2

        # list that tells the row and column pointer how to move after every pick.
        self.row_move = ([0] * (len(players) - 1)) + [1] + ([0] * (len(players) - 1)) + [1]
        self.column_move = ([1] * (len(players) - 1)) + [0] + [-1] * ((len(players) - 1)) + [0]
     
    def valid_input(self, mention : str, card : tuple) -> bool:
        
        """This checks if the card and user are valid."""

        # invalid user 
        if mention != self.players[self.active_player_index]:
            return "You are not the active drafter. Please wait until it is your turn."
        
        # card does not exists
        if not scryfallapi.card_exists(card):
            return "This card does not exist."
                        
        # after using source of truth card was already picked    
        if scryfallapi.get_fuzzied_correct(card) in self.card_tracker.get_cards():
            return "That card has already been chosen. Please try again."

        return "valid"

    def pick(self, username : str, mention: str, card : tuple) -> str:

        """This functions as the pipeline for picking occurs.
        All others methods below are executed in series to execute a pick 
        in a proper fasion."""

        # ensures valid input
        valid = self.valid_input(mention, card)

        if valid != "valid":
            return valid

        # make the pick
        card_name = scryfallapi.get_fuzzied_correct(card)
        self.card_tracker.add_card(mention, card_name)         
        sheetapi.pick(card_name, self.row, self.column)
        
        # pipeline to update
        self.row_update()
        self.column_update()
        self.active_player_update()
        self.picks_remaining_update()
        
        return username + " has chosen " + card_name + ". " + self.players[self.active_player_index] + " is up."

    #####################################
    ###         PICK PIPELINE        ###
    #####################################

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

    def __init__(self, players : list):
        
        self.card_tracker = {}

        for player in players:
            self.card_tracker[player] = []

    def add_card(self, player : str, card_name : str):

        """This adds a card to our dictionary of lists."""

        self.card_tracker[player].append(card_name)

    def get_cards(self) -> list:

        """This gets the list of all of the cards that were chosen."""

        all_picks = []

        for player in self.card_tracker:
            all_picks += self.card_tracker[player]

        return all_picks