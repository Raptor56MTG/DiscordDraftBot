from botBackend.draft_logic import DraftLogic, Player
import unittest
from unittest.mock import patch
import random
from decouple import config


class TestDraftLogic(unittest.TestCase):

    #####################################
    ###          CANCEL TESTS         ###
    #####################################

    def test_cancel_draft_not_setup(self):

        """Tests cancelled a draft when one was never set up"""

        logic = DraftLogic()
        actual = logic.cancel_draft()
        expected = "You cannot cancel a draft that's not set up."
        self.assertEqual(actual, expected)

    def test_cancel_draft_players_joined(self):

        """tests cancelled a draft when players have joined"""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        logic.join_draft("player_1", "1")
        actual = logic.cancel_draft()
        expected = "All players must leave the draft for it to be cancelled."
        self.assertEqual(actual, expected)

    def test_cancel_draft_already_fired(self):

        """Tests cancelling a draft when it already fired"""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.fire_draft()
                actual = logic.cancel_draft()
                expected = "You cannot cancel a draft that has fired."
                self.assertEqual(actual, expected)

    def test_cancel_draft_valid_1(self):

        """Tests cancelling a draft under valid circumstances"""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        actual = logic.cancel_draft()
        expected = "The draft setup has been cancelled."
        self.assertEqual(actual, expected)

    def test_cancel_draft_valid_2(self):

        """Tests cancelling a draft under valid circumstances"""

        logic = DraftLogic()

        logic.setup_draft("4", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")

        logic.leave_draft("player1", "1")
        logic.leave_draft("player2", "2")
        logic.leave_draft("player3", "3")
        logic.leave_draft("player4", "4")

        logic.cancel_draft()

        actual = logic.players
        expected = []

        self.assertEqual(actual, expected)

    def test_cancel_draft_valid_3(self):

        """Tests cancelling a draft under valid circumstances"""

        logic = DraftLogic()

        logic.setup_draft("4", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")

        logic.leave_draft("player1", "1")
        logic.leave_draft("player2", "2")
        logic.leave_draft("player3", "3")
        logic.leave_draft("player4", "4")

        logic.cancel_draft()

        actual = logic.picks
        expected = {}

        self.assertEqual(actual, expected)

    #####################################
    ###           INFO TESTS          ###
    #####################################

    def test_info_draft_setup(self):

        """Tests output of draft info when set up."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.join_draft("tester", "1")
        actual = logic.info_draft()
        expected = ("```player_count is: 4\n" +
                    "pick_count is: 45\n" +
                    "draft_fired status is: False\n" +
                    "format is: freeform\n" +
                    "Current joined drafters are:\n" +
                    "tester\n" + "```")
        self.assertEqual(actual, expected)

    def test_info_draft_not_setup(self):

        """Tests output of trying to get draft info when it has not been set up."""

        logic = DraftLogic()
        actual = logic.info_draft()
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    def test_info_cancel_draft(self):

        """Tests output of trying to get draft info after it has been cancelled."""

        logic = DraftLogic()

        logic.setup_draft("4", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")

        logic.leave_draft("player1", "1")
        logic.leave_draft("player2", "2")
        logic.leave_draft("player3", "3")
        logic.leave_draft("player4", "4")

        logic.cancel_draft()

        actual = logic.info_draft()
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    def test_info_empty(self):

        """Tests output of trying to get draft info after people join
        then leave and it is empty and not cancelled."""

        logic = DraftLogic()

        logic.setup_draft("4", "45", "modern")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")

        logic.leave_draft("player1", "1")
        logic.leave_draft("player2", "2")
        logic.leave_draft("player3", "3")
        logic.leave_draft("player4", "4")

        actual = logic.info_draft()
        expected = ("```player_count is: 4\n" +
                    "pick_count is: 45\n" +
                    "draft_fired status is: False\n" +
                    "format is: modern\n" +
                    "Current joined drafters are:\n" +
                    "```")

        self.assertEqual(actual, expected)

    #####################################
    ###           FIRE TESTS          ###
    #####################################

    def test_fire_draft_already_fired(self):

        """Tests trying to fire a draft when it has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.fire_draft()
                actual = logic.fire_draft()
                expected = "The draft has already fired."
                self.assertEqual(actual, expected)

    def test_fire_draft_not_setup(self):

        """Tests trying to fire a draft when it is not setup."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                actual = logic.fire_draft()
                expected = "The draft has not been set up."
                self.assertEqual(actual, expected)

    def test_fire_draft_not_full(self):

        """Tests trying to fire a draft without filling it up."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                actual = logic.fire_draft()
                expected = "Please ensure that the draft is full."
                self.assertEqual(actual, expected)

    def test_fire_draft_valid_1(self):

        """Tests firing the draft with valid criteria. Checks fire variable."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("3", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.fire_draft()

                self.assertTrue(logic.draft_fired)

    def test_fire_draft_valid_2(self):

        """Tests firing the draft with valid criteria. Checks string return."""

        # Use a seed to ensure the random call in the fire
        # method is always the same.
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("3", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                actual = logic.fire_draft()
                expected = ("Setup has been completed.\n\nSheet is available here: " +
                            f"{config('DOCS_LINK')}\n\n" +
                            "player_3 is up first.")

                self.assertEqual(actual, expected)

    def test_fire_draft_valid_3(self):

        """Ensures all setup values are correct upon firing."""

        # Use a seed to ensure the random call in the fire
        # method is always the same.
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("3", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.join_draft("player3", "3")

                logic.fire_draft()

                self.assertTrue(logic.draft_fired)
                self.assertTrue(logic.setup)
                self.assertEqual(logic.player_count, 3)
                self.assertEqual(logic.pick_count, 45)
                self.assertEqual(logic.active_player_index, 0)
                self.assertEqual(logic.row, 2)
                self.assertEqual(logic.column, 2)
                self.assertEqual(logic.picks_remaining, 135)

                expected_row_move = [0, 0, 1, 0, 0, 1]
                self.assertEqual(logic.row_move, expected_row_move)

                expected_column_move = [1, 1, 0, -1, -1, 0]
                self.assertEqual(logic.column_move, expected_column_move)

                expected_picks = {Player(username="player1", user_id="1"): [],
                                  Player(username="player2", user_id="2"): [],
                                  Player(username="player3", user_id="3"): []}

                self.assertEqual(logic.picks, expected_picks)

                expected_prepicks = {Player(username="player1", user_id="1"): [],
                                     Player(username="player2", user_id="2"): [],
                                     Player(username="player3", user_id="3"): []}

                self.assertEqual(logic.prepicks, expected_prepicks)

                expected_snake_player_list = [Player(username='player3', user_id='3'),
                                              Player(username='player2', user_id='2'),
                                              Player(username='player1', user_id='1'),
                                              Player(username='player1', user_id='1'),
                                              Player(username='player2', user_id='2'),
                                              Player(username='player3', user_id='3')]

                self.assertEqual(logic.snake_player_list, expected_snake_player_list)

                expected_players = [Player(username="player3", user_id="3"),
                                    Player(username="player2", user_id="2"),
                                    Player(username="player1", user_id="1")]

                self.assertListEqual(logic.players, expected_players)

    #####################################
    ###           JOIN TESTS          ###
    #####################################

    def test_join_draft_already_fired(self):

        """Tests trying to join when the draft has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.join_draft("player3", "3")
                expected = "The draft has already fired and cannot be joined."
                self.assertEqual(actual, expected)

    def test_join_draft_not_setup(self):

        """Tests trying to join when draft is not setup."""

        logic = DraftLogic()
        actual = logic.join_draft("player1", "1")
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    def test_join_draft_already_joined(self):

        """Tests trying to join draft twice."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.join_draft("player_1", "1")
        actual = logic.join_draft("player_1", "1")
        expected = "player_1 has already been added to the draft."
        self.assertEqual(actual, expected)

    def test_join_draft_full(self):

        """Tests trying to join draft when it is full."""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.join_draft("player3", "3")
        expected = "The draft is full. Please join the next draft!"
        self.assertEqual(actual, expected)

    def test_join_draft_valid_1(self):

        """Tests trying to join draft when valid and getting return value."""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        actual = logic.join_draft("player_1", "1")
        expected = "player_1 has been added to the draft."
        self.assertEqual(actual, expected)

    def test_join_draft_valid_2(self):

        """Tests trying to join draft when valid and getting list of players."""

        logic = DraftLogic()

        logic.setup_draft("8", "45", "freeform")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")
        logic.join_draft("player6", "6")
        logic.join_draft("player7", "7")
        logic.join_draft("player8", "8")

        actual = logic.players

        expected = [Player(username='player1', user_id='1'),
                    Player(username='player2', user_id='2'),
                    Player(username='player3', user_id='3'),
                    Player(username='player4', user_id='4'),
                    Player(username='player5', user_id='5'),
                    Player(username='player6', user_id='6'),
                    Player(username='player7', user_id='7'),
                    Player(username='player8', user_id='8')]

        self.assertEqual(actual, expected)

    def test_join_draft_valid_3(self):

        """Tests trying to join draft when valid and getting dictionary for picks."""

        logic = DraftLogic()

        logic.setup_draft("8", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")
        logic.join_draft("player6", "6")
        logic.join_draft("player7", "7")
        logic.join_draft("player8", "8")

        actual = logic.picks

        expected = {Player(username='player1', user_id='1'): [],
                    Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): [],
                    Player(username='player6', user_id='6'): [],
                    Player(username='player7', user_id='7'): [],
                    Player(username='player8', user_id='8'): []}

        self.assertEqual(actual, expected)

    def test_join_draft_valid_4(self):

        """Tests trying to join draft when valid and
        getting dictionary for prepicks."""

        logic = DraftLogic()

        logic.setup_draft("8", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")
        logic.join_draft("player6", "6")
        logic.join_draft("player7", "7")
        logic.join_draft("player8", "8")

        actual = logic.prepicks

        expected = {Player(username='player1', user_id='1'): [],
                    Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): [],
                    Player(username='player6', user_id='6'): [],
                    Player(username='player7', user_id='7'): [],
                    Player(username='player8', user_id='8'): []}

        self.assertEqual(actual, expected)

    #####################################
    ###          LEAVE TESTS          ###
    #####################################

    def test_leave_already_fired(self):

        """Tests trying to leave the draft when it has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.leave_draft("player1", "1")
                expected = "The draft has already fired and must be finished."
                self.assertEqual(actual, expected)

    def test_leave_draft_not_joined(self):

        """Tests trying to leave when you have not joined."""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.leave_draft("player3", "3")
        expected = "You cannot leave the draft if you never joined."
        self.assertEqual(actual, expected)

    def test_leave_draft_valid_1(self):

        """Tests trying to leave when valid and checking return value."""

        logic = DraftLogic()
        logic.setup_draft("2", "45", "freeform")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.leave_draft("player1", "1")
        expected = "player1 has left the draft."
        self.assertEqual(actual, expected)

    def test_leave_draft_valid_2(self):

        """Tests trying to leave when valid and checking drafters list variable."""

        logic = DraftLogic()

        logic.setup_draft("5", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")

        actual = logic.players

        expected = [Player(username='player1', user_id='1'),
                    Player(username='player2', user_id='2'),
                    Player(username='player3', user_id='3'),
                    Player(username='player4', user_id='4'),
                    Player(username='player5', user_id='5')]

        self.assertEqual(actual, expected)

        logic.leave_draft("player1", "1")

        actual = logic.players

        expected = [Player(username='player2', user_id='2'),
                    Player(username='player3', user_id='3'),
                    Player(username='player4', user_id='4'),
                    Player(username='player5', user_id='5')]

        self.assertEqual(actual, expected)

    def test_leave_draft_valid_3(self):

        """Tests trying to leave when valid and checking drafters list variable."""

        logic = DraftLogic()

        logic.setup_draft("5", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")

        actual = logic.picks

        expected = {Player(username='player1', user_id='1'): [],
                    Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): []}

        self.assertEqual(actual, expected)

        logic.leave_draft("player1", "1")

        actual = logic.picks

        expected = {Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): []}

        self.assertEqual(actual, expected)

    def test_leave_draft_valid_4(self):

        """Tests trying to leave when valid and checking
        prepicks."""

        logic = DraftLogic()

        logic.setup_draft("5", "45", "freeform")

        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")

        actual = logic.prepicks

        expected = {Player(username='player1', user_id='1'): [],
                    Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): []}

        self.assertEqual(actual, expected)

        logic.leave_draft("player1", "1")

        actual = logic.prepicks

        expected = {Player(username='player2', user_id='2'): [],
                    Player(username='player3', user_id='3'): [],
                    Player(username='player4', user_id='4'): [],
                    Player(username='player5', user_id='5'): []}

        self.assertEqual(actual, expected)

    #####################################
    ###       SETUP DRAFT TESTS       ###
    #####################################

    def test_setup_draft_already_fired(self):

        """Tests setting up a draft when it has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.setup_draft("4", "45", "freeform")
                expected = ("The draft has already fired. Please wait for " +
                            "it to be finished before starting another draft.")
                self.assertEqual(actual, expected)

    def test_setup_draft_already_setup(self):

        """Tests setting up a draft when one is already set up."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.setup_draft("4", "45", "freeform")
        expected = ("The draft setup has already been completed. " +
                    "To modify the setup use the edit commands.")
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_1(self):

        """Tests setting up a draft with invalid input for player count."""

        logic = DraftLogic()
        actual = logic.setup_draft("-1", "45", "freeform")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_2(self):

        """Tests setting up a draft with invalid input for pick count."""

        logic = DraftLogic()
        actual = logic.setup_draft("5", "1000", "freeform")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_3(self):

        """Tests setting up a draft with invalid input for player count."""

        logic = DraftLogic()
        actual = logic.setup_draft("wwwwww", "45", "freeform")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_4(self):

        """Tests setting up a draft with invalid input for pick count."""

        logic = DraftLogic()
        actual = logic.setup_draft("5", "ergd", "freeform")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_5(self):

        """Tests setting up a draft with invalid input for format."""

        logic = DraftLogic()
        actual = logic.setup_draft("5", "ergd", "aesrdgfh")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_1(self):

        """Tests valid setup and checking return value."""

        logic = DraftLogic()
        actual = logic.setup_draft("5", "50", "freeform")
        expected = ("The draft has been set up. We have 5 players, 50 " +
                    "picks, and the format is freeform. Use the " +
                    "!join command to be added to the draft.")
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_2(self):

        """Tests valid setup and checking player count"""

        logic = DraftLogic()
        logic.setup_draft("5", "50", "freeform")
        actual = logic.player_count
        expected = 5
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_3(self):

        """Tests valid setup and checking pick count"""

        logic = DraftLogic()
        logic.setup_draft("5", "50", "freeform")
        actual = logic.pick_count
        expected = 50
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_4(self):

        """Tests valid setup and checking setup value"""

        logic = DraftLogic()
        logic.setup_draft("5", "50", "freeform")
        actual = logic.setup
        expected = True
        self.assertEqual(actual, expected)

    #####################################
    ###       EDIT PLAYER TESTS       ###
    #####################################

    def test_edit_player_already_fired(self):

        """Tests editing a draft when it has already fire."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.edit_player("6")
                expected = "The draft has already fired. It cannot be edited."
                self.assertEqual(actual, expected)

    def test_edit_player_draft_not_setup(self):

        """Tests editing players when draft has not been set up."""

        logic = DraftLogic()
        actual = logic.edit_player("5")
        expected = "The draft has not been set up. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_1(self):

        """Tests editing a draft with invalid input"""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_player("wwww")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_2(self):

        """Tests editing player count with invalid input"""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_player("456778")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_3(self):

        """Tests editing player count with invalid input"""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_player("-66")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_valid_1(self):

        """Tests editing a draft with valid input for pick count"""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_player("5")
        expected = "Player count is: 5"
        self.assertEqual(actual, expected)

    def test_edit_player_valid_2(self):

        """Tests editing a draft with valid input for player count"""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.edit_player("5")
        actual = logic.player_count
        expected = 5
        self.assertEqual(actual, expected)

    def test_edit_player_too_small(self):

        """Tests editing a draft with valid input for player
        count but is smaller than the current number of
        players in the draft queue. """

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.join_draft("player_3", "3")
        logic.join_draft("player_4", "4")
        actual = logic.edit_player("3")
        expected = ("The draft currently has too many players to go to 3" +
                    " players. Please have players leave before making the edit.")
        self.assertEqual(actual, expected)

    #####################################
    ###        EDIT PICK TESTS        ###
    #####################################

    def test_edit_pick_already_fired(self):

        """Tests editing a draft when it has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.edit_pick("6")
                expected = "The draft has already fired. It cannot be edited."
                self.assertEqual(actual, expected)

    def test_edit_pick_draft_not_setup(self):

        """Tests editing players when draft has not been set up."""

        logic = DraftLogic()
        actual = logic.edit_pick("5")
        expected = "The draft has not been set up. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_1(self):

        """Tests editing a draft with invalid input."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_pick("wwww")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_2(self):

        """Tests editing player count with invalid input."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_pick("456778")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_3(self):

        """Tests editing pick count with invalid input."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_pick("-66")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_valid_1(self):

        """Tests editing a draft with valid input for pick count."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_pick("50")
        expected = "Pick count is: 50"
        self.assertEqual(actual, expected)

    def test_edit_pick_valid_2(self):

        """Tests editing a draft with valid input for player count."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.edit_pick("50")
        actual = logic.pick_count
        expected = 50
        self.assertEqual(actual, expected)

    #####################################
    ###       EDIT FORMAT TESTS       ###
    #####################################

    def test_edit_format_already_fired(self):

        """Tests editing a draft when it has already fired."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")
                logic.fire_draft()
                actual = logic.edit_format("modern")
                expected = "The draft has already fired. It cannot be edited."
                self.assertEqual(actual, expected)

    def test_edit_format_draft_not_setup(self):

        """Tests editing players when draft has not been set up."""

        logic = DraftLogic()
        actual = logic.edit_format("legacy")
        expected = "The draft has not been set up. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_format_invalid_input_1(self):

        """Tests editing a draft with invalid input."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_format("magical format")
        expected = "Invalid parameters. Please use the '!help edit_format' command for details."
        self.assertEqual(actual, expected)

    def test_edit_format_valid_1(self):

        """Tests editing a draft with valid input for format."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        actual = logic.edit_format("LEGACy")
        expected = "Format is: legacy"
        self.assertEqual(actual, expected)

    def test_edit_format_valid_2(self):

        """Tests editing a draft with valid input for format."""

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.edit_format("modern")
        actual = logic.format
        expected = "modern"
        self.assertEqual(actual, expected)

    #####################################
    ###      PICK PIPELINE TESTS      ###
    #####################################

    def test_row_update(self):

        """Ensures the row updates correctly."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.row
                expected = 2
                self.assertEqual(actual, expected)

                logic.row_update()  # 2
                logic.active_player_update()
                actual = logic.row
                expected = 2
                self.assertEqual(actual, expected)

                logic.row_update()  # 2
                logic.active_player_update()
                actual = logic.row
                expected = 2
                self.assertEqual(actual, expected)

                logic.row_update()  # 2
                logic.active_player_update()
                actual = logic.row
                expected = 2
                self.assertEqual(actual, expected)

                logic.row_update()  # 3
                logic.active_player_update()
                actual = logic.row
                expected = 3
                self.assertEqual(actual, expected)

                logic.row_update()  # 3
                logic.active_player_update()
                actual = logic.row
                expected = 3
                self.assertEqual(actual, expected)

                logic.row_update()  # 3
                logic.active_player_update()
                actual = logic.row
                expected = 3
                self.assertEqual(actual, expected)

                logic.row_update()  # 3
                logic.active_player_update()
                actual = logic.row
                expected = 3
                self.assertEqual(actual, expected)

                logic.row_update()  # 4
                logic.active_player_update()
                actual = logic.row
                expected = 4
                self.assertEqual(actual, expected)

    def test_column_update(self):

        """Ensures the column updates correctly."""

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.column  # 2
                expected = 2
                self.assertEqual(actual, expected)

                logic.column_update()  # 3
                logic.active_player_update()
                actual = logic.column
                expected = 3
                self.assertEqual(actual, expected)

                logic.column_update()  # 4
                logic.active_player_update()
                actual = logic.column
                expected = 4
                self.assertEqual(actual, expected)

                logic.column_update()  # 5
                logic.active_player_update()
                actual = logic.column
                expected = 5
                self.assertEqual(actual, expected)

                logic.column_update()  # 5
                logic.active_player_update()
                actual = logic.column
                expected = 5
                self.assertEqual(actual, expected)

                logic.column_update()  # 4
                logic.active_player_update()
                actual = logic.column
                expected = 4
                self.assertEqual(actual, expected)

                logic.column_update()  # 3
                logic.active_player_update()
                actual = logic.column
                expected = 3
                self.assertEqual(actual, expected)

                logic.column_update()  # 2
                logic.active_player_update()
                actual = logic.column
                expected = 2
                self.assertEqual(actual, expected)

                logic.column_update()  # 2
                logic.active_player_update()
                actual = logic.column
                expected = 2
                self.assertEqual(actual, expected)

                logic.column_update()  # 3
                logic.active_player_update()
                actual = logic.column
                expected = 3
                self.assertEqual(actual, expected)

    def test_active_player_update(self):

        """Ensures the active player index updates as intended.
        This follows a snake like pattern."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_1', '1')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 3
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_3', '3')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 4
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_4', '4')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 2
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_2', '2')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 2
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_2', '2')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 4
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_4', '4')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 3
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_3', '3')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 1
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_1', '1')
                self.assertEqual(actual, expected)

                logic.active_player_update()  # 1
                actual = logic.snake_player_list[logic.active_player_index]
                expected = Player('player_1', '1')
                self.assertEqual(actual, expected)

    def test_picks_remaining_update(self):

        """Ensures picks remaining updates as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                logic.picks_remaining_update()
                logic.picks_remaining_update()
                logic.picks_remaining_update()
                logic.picks_remaining_update()
                logic.picks_remaining_update()

                actual = logic.picks_remaining
                expected = 175  # 45 * 4 - 4 = 175

                self.assertEqual(actual, expected)

    #####################################
    ###       INVALID PICK TESTS      ###
    #####################################

    def test_invalid_pick_not_active_player(self):

        """Tests invalid input with player who went out of order."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi'):

                    actual = logic.invalid_pick('player_2', '2', {'object': 'card', 'name': 'Gush'})
                    expected = "You are not the active drafter. Please wait until it is your turn."
                    self.assertEqual(actual, expected)

    def test_invalid_pick_card_doesnt_exist(self):

        """Tests invalid input with non existent card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_pick('player_1', '1', {'object': 'error'})
                expected = "This card does not exist."
                self.assertEqual(actual, expected)

    def test_invalid_pick_card_already_picked(self):

        """Tests invalid input with a non unique card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi'):

                    logic.picks[Player('player_2', '2')].append("Gush")
                    actual = logic.invalid_pick('player_1', '1', {'object': 'card', 'name': 'Gush'})

                    expected = "That card has already been chosen. Please try again."
                    self.assertEqual(actual, expected)

    def test_invalid_pick_invalid_format(self):

        """Tests invalid input with non existent card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "modern")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_pick('player_1', '1',
                                            {'object': 'card', 'name': 'Gush',
                                             'legalities': {'modern': 'not_legal'}})
                expected = "This card is not legal in modern."
                self.assertEqual(actual, expected)

    def test_invalid_pick_not_fired(self):

        """Tests invalid input when not fired."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        logic = DraftLogic()
        logic.setup_draft("4", "45", "freeform")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.join_draft("player_3", "3")
        logic.join_draft("player_4", "4")

        actual = logic.invalid_pick('player_1', '1', {'object': 'card', 'name': 'Gush'})

        expected = "You cannot make picks until the draft has fired."
        self.assertEqual(actual, expected)

    def test_invalid_pick_valid(self):

        """Tests invalid input with valid input."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi'):

                    actual = logic.invalid_pick('player_1', '1', {'object': 'card', 'name': 'Gush'})
                    self.assertIsNone(actual)

    #####################################
    ###       PICK TRACKER TESTS      ###
    #####################################

    def test_pick_tracker_add_card(self):

        """Ensures the card tracker works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pick('player_3', '3', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pick('player_4', '4', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pick('player_2', '2', ('Swamp',))

                    expected = {Player('player_1', '1'): ['Gush'],
                                Player('player_2', '2'): ['Swamp'],
                                Player('player_3', '3'): ['Ponder'],
                                Player('player_4', '4'): ['Skred']}

                    actual = logic.picks
                    self.assertEqual(actual, expected)

    #####################################
    ###        PRE PICK TESTS       ###
    #####################################

    def test_pre_pick(self):

        """Ensures prepick works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pre_pick('player_3', '3', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pre_pick('player_4', '4', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pre_pick('player_2', '2', ('Swamp',))

                    expected = {Player('player_1', '1'): ['Gush'],
                                Player('player_2', '2'): ['Swamp'],
                                Player('player_3', '3'): ['Ponder'],
                                Player('player_4', '4'): ['Skred']}

                    actual = logic.prepicks
                    self.assertEqual(actual, expected)

    def test_iterate_pre_pick_1(self):

        """Ensures prepick works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pre_pick('player_3', '3', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pre_pick('player_4', '4', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pre_pick('player_2', '2', ('Swamp',))

                    actual = logic.iterate_prepicks()
                    expected = [('player_1', 'Gush'),
                                ('player_3', 'Ponder'),
                                ('player_4', 'Skred'),
                                ('player_2', 'Swamp')]
                    self.assertEqual(actual, expected)

                    actual = logic.picks_remaining
                    expected = 176
                    self.assertEqual(actual, expected)

    def test_iterate_pre_pick_2(self):

        """Ensures prepick works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    logic.picks_remaining = 3

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pre_pick('player_3', '3', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pre_pick('player_4', '4', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pre_pick('player_2', '2', ('Swamp',))

                    actual = logic.iterate_prepicks()
                    expected = [('player_1', 'Gush'),
                                ('player_3', 'Ponder'),
                                ('player_4', 'Skred')]
                    self.assertEqual(actual, expected)

    #####################################
    ###   CANCEL PICK TRACKER TESTS   ###
    #####################################

    def test_cancel_pre_pick(self):

        """Ensures cancel prepick works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pre_pick('player_3', '3', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pre_pick('player_4', '4', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pre_pick('player_2', '2', ('Swamp',))

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    actual = logic.cancel_pre_pick('player_1', '1', ("Gush",))
                    expected = 'You have successfully removed: Gush.'
                    self.assertEqual(actual, expected)

                    expected = {Player('player_1', '1'): [],
                                Player('player_2', '2'): ['Swamp'],
                                Player('player_3', '3'): ['Ponder'],
                                Player('player_4', '4'): ['Skred']}

                    actual = logic.prepicks
                    self.assertEqual(actual, expected)

    #####################################
    ###      GET PREPICKS TESTS       ###
    #####################################

    def test_get_pre_picks_not_fired(self):

        """Ensures prepicks work as intended."""

        logic = DraftLogic()

        actual = logic.get_pre_picks('player_1', '1')
        expected = "No pre-picks as draft has not fired."
        self.assertEqual(actual, expected)

    def test_get_pre_picks_invalid_player(self):

        """Ensures the card tracker works as intended."""
        """Ensures the get prepicks works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.get_pre_picks('player_5', '5')
                expected = "You are not in this draft and have no pre-picks."

                self.assertEqual(actual, expected)

    def test_get_pre_picks_empty(self):

        """Ensures the get prepicks works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.get_pre_picks('player_1', '1')
                expected = "Pre-pick queue is empty."

                self.assertEqual(actual, expected)

    def test_get_pre_picks_valid(self):

        """Ensures the get prepicks works as intended."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))
                    mock_api.return_value = {'object': 'card', 'name': 'Ponder'}
                    logic.pre_pick('player_1', '1', ('Ponder',))
                    mock_api.return_value = {'object': 'card', 'name': 'Skred'}
                    logic.pre_pick('player_1', '1', ('Skred',))
                    mock_api.return_value = {'object': 'card', 'name': 'Swamp'}
                    logic.pre_pick('player_1', '1', ('Swamp',))

                    actual = logic.get_pre_picks('player_1', '1')
                    expected = '```1. Gush\n2. Ponder\n3. Skred\n4. Swamp\n```'

                    self.assertEqual(actual, expected)

    #####################################
    ###    INVALID PRE-PICK TESTS     ###
    #####################################

    def test_invalid_prepick_not_in_draft(self):

        """Tests invalid input with player who is not in draft."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_prepick('player_5', '5', {'object': 'card', 'name': 'Gush'})
                expected = "You are not in this draft and cannot make pre-picks."
                self.assertEqual(actual, expected)

    def test_invalid_prepick_card_doesnt_exist(self):

        """Tests invalid input with non existent card"""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_prepick('player_1', '1', {'object': 'error'})
                expected = "This card does not exist."
                self.assertEqual(actual, expected)

    def test_invalid_prepick_not_fired(self):

        """Tests invalid input when not fired"""

        logic = DraftLogic()

        actual = logic.invalid_prepick('player_1', '1', {'object': 'card', 'name': 'Gush'})

        expected = "You cannot make pre-picks until the draft has fired."
        self.assertEqual(actual, expected)

    def test_invalid_prepick_valid(self):

        """Tests invalid input with valid input"""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_prepick('player_1', '1', {'object': 'card', 'name': 'Gush'})
                self.assertIsNone(actual)

    def test_invalid_prepick_already_picked(self):

        """Tests invalid input with a non unique card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                logic.picks[Player('player_2', '2')].append("Gush")
                actual = logic.invalid_prepick('player_1', '1', {'object': 'card', 'name': 'Gush'})

                expected = "That card has already been chosen in the draft. Please try again."
                self.assertEqual(actual, expected)

    def test_invalid_prepick_already_prepicked(self):

        """Tests invalid input with a non unique prepick card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                logic.prepicks[Player('player_1', '1')].append("Gush")
                actual = logic.invalid_prepick('player_1', '1', {'object': 'card', 'name': 'Gush'})

                expected = "You have already pre-picked this card. Please try again."
                self.assertEqual(actual, expected)

    def test_invalid_prepick_invalid_format(self):

        """Tests invalid input with non existent card."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "modern")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_prepick('player_4', '4', {'object': 'card', 'name': 'Gush',
                                               'legalities': {'modern': 'not_legal'}})
                expected = "This card is not legal in modern."
                self.assertEqual(actual, expected)

    #####################################
    ###     INVALID CANCEL PRE-PICK   ###
    #####################################

    def test_invalid_cancel_prepick_not_in_draft(self):

        """Tests invalid input with player who is not in draft."""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_cancel_prepick(
                    'player_5', '5', {'object': 'card', 'name': 'Gush'})
                expected = "You are not in this draft and cannot cancel pre-picks."
                self.assertEqual(actual, expected)

    def test_invalid_cancel_prepick_card_doesnt_exist(self):

        """Tests invalid input with non existent card"""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_cancel_prepick('player_1', '1', {'object': 'error'})
                expected = "This card does not exist."
                self.assertEqual(actual, expected)

    def test_invalid_cancel_prepick_not_fired(self):

        """Tests invalid input when not fired"""

        logic = DraftLogic()

        actual = logic.invalid_cancel_prepick('player_1', '1', {'object': 'card', 'name': 'Gush'})

        expected = "You cannot cancel pre-picks until the draft has fired."
        self.assertEqual(actual, expected)

    def test_invalid_cancel_prepick_not_pre_picked(self):

        """Tests invalid input with valid input"""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                actual = logic.invalid_cancel_prepick(
                    'player_1', '1', {'object': 'card', 'name': 'Gush'})
                expected = "Cannot remove cards you have not pre-picked."
                self.assertEqual(actual, expected)

    def test_invalid_cancel_prepick_valid(self):

        """Tests invalid input with valid input"""

        # Use a seed to ensure the random call in the fire
        # method is always the same. (1 3 4 2 2 4 3 1)
        random.seed(100)

        logic = DraftLogic()

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("4", "45", "freeform")
                logic.join_draft("player_1", "1")
                logic.join_draft("player_2", "2")
                logic.join_draft("player_3", "3")
                logic.join_draft("player_4", "4")
                logic.fire_draft()

                # use mock to ensure we don't call scryfall api.
                with patch('botBackend.draft_logic.scryfallapi.get_scryfall_json') as mock_api:

                    mock_api.return_value = {'object': 'card', 'name': 'Gush'}
                    logic.pre_pick('player_1', '1', ('Gush',))

                    actual = logic.invalid_cancel_prepick(
                        'player_1', '1', {'object': 'card', 'name': 'Gush'})
                    self.assertIsNone(actual)

    #####################################
    ###           RESET TESTS         ###
    #####################################

    def test_reset(self):

        """Tests the reset method once a draft is finished."""

        # Use a seed to ensure the random call in the fire
        # method is always the same.
        random.seed(100)

        # use mock to ensure we don't call google sheet api
        with patch('botBackend.draft_logic.sheetapi'):
            with patch('botBackend.draft_logic.backup'):
                logic = DraftLogic()
                logic.setup_draft("2", "45", "freeform")
                logic.join_draft("player1", "1")
                logic.join_draft("player2", "2")

                actual = logic.fire_draft()
                expected = ("Setup has been completed.\n\nSheet is available here: " +
                            f"{config('DOCS_LINK')}\n\n" +
                            "player2 is up first.")

                self.assertEqual(actual, expected)

                logic.reset()

                self.assertFalse(logic.draft_fired)
                self.assertFalse(logic.setup)
                self.assertIsNone(logic.format)
                self.assertEqual(logic.player_count, 0)
                self.assertEqual(logic.pick_count, 0)
                self.assertEqual(logic.picks, {})
                self.assertEqual(logic.prepicks, {})
                self.assertEqual(logic.players, [])
                self.assertEqual(logic.active_player_index, 0)
                self.assertEqual(logic.row, 2)
                self.assertEqual(logic.column, 2)
                self.assertEqual(logic.row_move, [])
                self.assertEqual(logic.column_move, [])
                self.assertEqual(logic.picks_remaining, 0)
                self.assertEqual(logic.snake_player_list, [])


if __name__ == "__main__":
    unittest.main()
