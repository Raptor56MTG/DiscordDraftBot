import unittest
from botBackend.draft_pick_logic import DraftPickLogic, CardTracker

class TestDraftPickLogic(unittest.TestCase):
    
    #####################################
    ###         PROPERTY TESTS        ###
    #####################################

    def test_column_move(self):
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)

        expected = [1, 1, 1, 0, -1, -1, -1, 0]
        actual = draft_pick_logic.column_move

        self.assertEqual(expected, actual)

    def test_row_move(self):
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)

        expected = [0, 0, 0, 1, 0, 0, 0, 1]
        actual = draft_pick_logic.row_move

        self.assertEqual(expected, actual)

    #####################################
    ###       CARD TRACKER TESTS      ###
    #####################################

    def test_card_tracker_add_card(self):

        """Ensures the card tracker works as intended."""

        player_mentions = ['@1', '@2', '@3', '@4']

        card_tracker = CardTracker(player_mentions)

        card_tracker.add_card('@1', 'lightning bolt')
        card_tracker.add_card('@2', 'gush')
        card_tracker.add_card('@3', 'island')
        card_tracker.add_card('@4', 'swamp')
        card_tracker.add_card('@4', 'forest')
        card_tracker.add_card('@3', 'mountain')
        card_tracker.add_card('@2', 'ponder')
        card_tracker.add_card('@1', 'preordain')
        card_tracker.add_card('@1', 'unearth')
        card_tracker.add_card('@2', 'oko, thief of crowns')

        expected = {"@1": ['lightning bolt', 'preordain', 'unearth'],
                    "@2": ['gush', 'ponder', 'oko, thief of crowns'],
                    "@3": ['island', 'mountain'],
                    "@4": ['swamp', 'forest']}
        
        actual = card_tracker.card_tracker

        self.assertEqual(expected, actual)

    def test_card_tracker_get_cards(self):
        
        """Tests the get all method to return a list of all cards 
        in the draft."""
        
        player_mentions = ['@1', '@2', '@3', '@4']

        card_tracker = CardTracker(player_mentions)

        card_tracker.add_card('@1', 'Lightning Bolt')
        card_tracker.add_card('@2', 'Gush')
        card_tracker.add_card('@3', 'Island')
        card_tracker.add_card('@4', 'Swamp')
        card_tracker.add_card('@4', 'Forest')
        card_tracker.add_card('@3', 'Mountain')
        card_tracker.add_card('@2', 'Ponder')
        card_tracker.add_card('@1', 'Preordain')

        expected = ['Lightning Bolt', 'Preordain', 'Gush', 'Ponder', 
        'Island', 'Mountain', 'Swamp', 'Forest']
    
        actual = card_tracker.get_cards()
        
        self.assertEqual(expected, actual)

    #####################################
    ###       VALID INPUT TESTS       ###
    #####################################

    def test_valid_input_not_active_player(self):
        
        """Tests valid input with player who went out of order"""
        
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        actual = draft_pick_logic.valid_input('@2', ('Lightning Bolt',))
        expected = "You are not the active drafter. Please wait until it is your turn."
        self.assertEqual(expected, actual)

    def test_valid_input_card_doesnt_exist(self):
        
        """Tests valid input with non existent card"""
        
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        actual = draft_pick_logic.valid_input('@1', ('assdassdassdsdsdsd',))
        expected = "This card does not exist."
        self.assertEqual(expected, actual)

    def test_valid_input_card_already_picked(self):
        
        """Tests valid input with a non unique card."""
        
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        draft_pick_logic.card_tracker.add_card('@2', 'Island')
        actual = draft_pick_logic.valid_input('@1', ('Island',))
        expected = "That card has already been chosen. Please try again."
        self.assertEqual(expected, actual)

    def test_valid_input_valid(self):
        
        """Tests valid input with valid input"""
        
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        actual = draft_pick_logic.valid_input('@1', ('Island',))
        expected = None
        self.assertEqual(expected, actual)

    #####################################
    ###      PICK PIPELINE TESTS      ###
    #####################################

    def test_row_update(self):

        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)  # 2
        actual = draft_pick_logic.row
        expected = 2
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 2
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 2
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 2
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 2
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 2
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 2
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 3
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 3
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 3
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.row
        expected = 3
        self.assertEqual(expected, actual)

        draft_pick_logic.row_update()  # 4
        draft_pick_logic.active_player_update() 
        actual = draft_pick_logic.row
        expected = 4
        self.assertEqual(expected, actual)

    def test_column_update(self):
        
        """Ensures the column updates correctly."""
        
        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)  # 2
        actual = draft_pick_logic.column
        expected = 2
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 3
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 4
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 4
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 5
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 5
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 5
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 5
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 4
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 4
        self.assertEqual(expected, actual)

        draft_pick_logic.column_update()  # 3
        draft_pick_logic.active_player_update()
        actual = draft_pick_logic.column
        expected = 3
        self.assertEqual(expected, actual)

    def test_active_player_update(self):
        
        """Ensures the active player index updates as intended.
        This follows a snake like pattern."""

        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@1'
        self.assertEqual(actual, expected)
        
        draft_pick_logic.active_player_update()  # 2
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@2'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 3
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@3'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 4
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@4'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 4
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@4'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 3
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@3'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 2
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@2'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 1
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@1'
        self.assertEqual(actual, expected)

        draft_pick_logic.active_player_update()  # 1
        actual = draft_pick_logic.players[draft_pick_logic.active_player_index]
        expected = '@1'
        self.assertEqual(actual, expected)

    def test_picks_remaining_update(self):
        
        """Ensures picks remaining updates as intended"""

        player_mentions = ['@1', '@2', '@3', '@4']
        draft_pick_logic = DraftPickLogic(player_mentions, 45)
        draft_pick_logic.picks_remaining_update()
        draft_pick_logic.picks_remaining_update()
        draft_pick_logic.picks_remaining_update()
        draft_pick_logic.picks_remaining_update()
        draft_pick_logic.picks_remaining_update()

        actual = draft_pick_logic.picks_remaining
        expected = 175 # 45 * 4 - 4 = 175

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()