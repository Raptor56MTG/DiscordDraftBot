import gspread
from botBackend import scryfallapi 

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
        self.row_update = ([0] * (len(players) - 1)) + [1] + ([0] * (len(players) - 1)) + [1]
        self.column_update = ([1] * (len(players) - 1)) + [0] + [-1] * ((len(players) - 1)) + [0]
     
    def get_all_picks(self) -> list:

        """Returns a list of all of the current picks in the draft."""
        return self.card_tracker.get_cards()

    def pick(self, username : str, mention: str, card : tuple, sheet_api : object) -> str:

        """This functions as the pipeline for picking occurs.
        All others methods below are executed in series to execute a pick 
        in a proper fasion."""

        # if they are not the active player
        if mention != self.players[self.active_player_index]:
            return "You are not the active drafter. Please wait until it is your turn."
        
        # otherwise, try to make a pick
        else:
            # see if card exists 
            if scryfallapi.card_exists(card):
                
                # get the correct name to have a source of truth
                card_name = scryfallapi.get_fuzzied_correct(card)

                # see if it was already picked       
                if card_name not in self.card_tracker.get_cards():
                    
                    # pick the card 
                    self.card_tracker.add_card(mention, card_name) 
                    
                    # add card to sheets API
                    sheet_api.pick(card_name, self.row, self.column)
   
                    # update position for next pick
                    self.row += self.row_update[self.active_player_index]
                    self.column += self.column_update[self.active_player_index]

                    # update the active player index
                    self.active_player_index = (self.active_player_index + 1) % len(self.players)

                    # decrease number of picks left in the draft
                    self.picks_remaining -= 1
                    
                    return username + " has chosen " + card_name + ". " + self.players[self.active_player_index] + " is up."
                else:
                    return "That card has already been chosen. Please try again."
            else:
                return "This card does not exist."

class CardTracker():

    """This class acts as the data structure to track all of the cards.
    Thi is just a dictionary of linked lists."""

    def __init__(self, players : list):
        
        self.card_tracker = {}

        for player in players:
            self.card_tracker[player] = []

    def add_card(self, player : str, card_name : str):

        """This adds a card to our dictionary of linked lists."""

        self.card_tracker[player].append(card_name)

    def get_cards(self) -> list:

        """This gets the list of all of the cards that were chosen."""

        all_picks = []

        for player in self.card_tracker:
            all_picks += self.card_tracker[player]

        return all_picks