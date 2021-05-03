from botBackend.draft_setup_logic import DraftSetupLogic
import unittest


class TestDraftSetupLogic(unittest.TestCase):

    #####################################
    ###          CANCEL TESTS         ###
    #####################################

    def test_cancel_draft_not_setup(self):

        """Tests cancelled a draft when one was never set up"""

        logic = DraftSetupLogic()
        actual = logic.cancel_draft()
        expected = "You cannot cancel a draft that was not set up."
        self.assertEqual(actual, expected)

    def test_cancel_draft_players_joined(self):

        """tests cancelled a draft when players have joined"""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "40")
        logic.join_draft("player_1", "1")
        actual = logic.cancel_draft()
        expected = "All players must leave the draft for it to be cancelled."
        self.assertEqual(actual, expected)

    def test_cancel_draft_already_fired(self):

        """Tests cancelling a draft when it already fired"""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "40")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.fire_draft()
        actual = logic.cancel_draft()
        expected = "You cannot cancel a draft that has fired."
        self.assertEqual(actual, expected)

    def test_cancel_draft_valid(self):

        """Tests cancelling a draft under valid circumstances"""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "40")
        actual = logic.cancel_draft()
        expected = "The draft setup has been cancelled."
        self.assertEqual(actual, expected)

    #####################################
    ###           INFO TESTS          ###
    #####################################

    def test_info_draft_setup(self):

        """Tests output of draft info when set up."""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        logic.join_draft("tester", "1")
        actual = logic.info_draft()
        expected = ("```player_count is: 4\n" +
                    "pick_count is: 45\n" +
                    "draft_fired status is: False\n" +
                    "Current joined drafters are:\n" +
                    "tester\n" + "```")
        self.assertEqual(actual, expected)

    def test_info_draft_not_setup(self):

        """Tests output of trying to get draft info when it has not been set up."""

        logic = DraftSetupLogic()
        actual = logic.info_draft()
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    #####################################
    ###           FIRE TESTS          ###
    #####################################

    def test_fire_draft_already_fired(self):

        """Tests trying to fire a draft when it has already fired."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.fire_draft()
        actual = logic.fire_draft()
        expected = "The draft has already fired."
        self.assertEqual(actual, expected)

    def test_fire_draft_not_setup(self):

        """Tests trying to fire a draft when it is not setup."""

        logic = DraftSetupLogic()
        actual = logic.fire_draft()
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    def test_fire_draft_not_full(self):

        """Tests trying to fire a draft without filling it up."""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.fire_draft()
        expected = "Please ensure that the draft is full."
        self.assertEqual(actual, expected)

    def test_fire_draft_valid_1(self):

        """Tests firing the draft with valid criteria. Checks fire variable."""

        logic = DraftSetupLogic()
        logic.setup_draft("3", "45")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.join_draft("player_3", "3")
        logic.fire_draft()
        self.assertTrue(logic.draft_fired)

    def test_fire_draft_valid_2(self):

        """Tests firing the draft with valid criteria. Checks string return."""

        logic = DraftSetupLogic()
        logic.setup_draft("3", "45")
        logic.join_draft("player_1", "1")
        logic.join_draft("player_2", "2")
        logic.join_draft("player_3", "3")
        actual = logic.fire_draft()
        expected = ("The draft has fired and is currently being set up. " +
                    "All other commands are disabled until sheet setup is complete.")
        self.assertEqual(actual, expected)

    #####################################
    ###           JOIN TESTS          ###
    #####################################

    def test_join_draft_already_fired(self):

        """Tests trying to join when the draft has already fired."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.fire_draft()
        actual = logic.join_draft("player3", "3")
        expected = "The draft has already fired and cannot be joined."
        self.assertEqual(actual, expected)

    def test_join_draft_not_setup(self):

        """Tests trying to join when draft is not setup."""

        logic = DraftSetupLogic()
        actual = logic.join_draft("player1", "1")
        expected = "The draft has not been set up."
        self.assertEqual(actual, expected)

    def test_join_draft_already_joined(self):

        """Tests trying to join draft twice."""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        logic.join_draft("player_1", "1")
        actual = logic.join_draft("player_1", "1")
        expected = "player_1 has already been added to the draft."
        self.assertEqual(actual, expected)

    def test_join_draft_full(self):

        """Tests trying to join draft when it is full."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.join_draft("player3", "3")
        expected = "The draft is full. Please join the next draft!"
        self.assertEqual(actual, expected)

    def test_join_draft_valid_1(self):

        """Tests trying to join draft when valid and getting return value."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        actual = logic.join_draft("player_1", "1")
        expected = "player_1 has been added to the draft."
        self.assertEqual(actual, expected)

    def test_join_draft_valid_2(self):

        """Tests trying to join draft when valid and getting list of players."""

        logic = DraftSetupLogic()
        logic.setup_draft("8", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")
        logic.join_draft("player6", "6")
        logic.join_draft("player7", "7")
        logic.join_draft("player8", "8")
        actual = logic.players
        expected = {'1': 'player1',
                    '2': 'player2',
                    '3': 'player3',
                    '4': 'player4',
                    '5': 'player5',
                    '6': 'player6',
                    '7': 'player7',
                    '8': 'player8',
                    }

        self.assertEqual(actual, expected)

    #####################################
    ###          LEAVE TESTS          ###
    #####################################

    def test_leave_already_fired(self):

        """Tests trying to leave the draft when it has already fired."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.fire_draft()
        actual = logic.leave_draft("player1", "1")
        expected = "The draft has already fired and must be finished."
        self.assertEqual(actual, expected)

    def test_leave_draft_not_joined(self):

        """Tests trying to leave when you have not joined."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.leave_draft("player3", "3")
        expected = "You cannot leave the draft if you never joined."
        self.assertEqual(actual, expected)

    def test_leave_draft_valid_1(self):

        """Tests trying to leave when valid and checking return value."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        actual = logic.leave_draft("player1", "1")
        expected = "player1 has left the draft."
        self.assertEqual(actual, expected)

    def test_leave_draft_valid_2(self):

        """Tests trying to leave when valid and checking drafters list variable."""

        logic = DraftSetupLogic()
        logic.setup_draft("5", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.join_draft("player3", "3")
        logic.join_draft("player4", "4")
        logic.join_draft("player5", "5")
        logic.leave_draft("player1", "1")
        actual = logic.players
        expected = {'2': 'player2',
                    '3': 'player3',
                    '4': 'player4',
                    '5': 'player5',
                    }
        self.assertEqual(actual, expected)

    #####################################
    ###       SETUP DRAFT TESTS       ###
    #####################################

    def test_setup_draft_already_fired(self):

        """Tests setting up a draft when it has already fired."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.fire_draft()
        actual = logic.setup_draft("4", "45")
        expected = ("The draft has already fired. Please wait for " +
                    "it to be finished before starting another draft.")
        self.assertEqual(actual, expected)

    def test_setup_draft_already_setup(self):

        """Tests setting up a draft when one is already set up."""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.setup_draft("4", "45")
        expected = ("The draft setup has already been completed. " +
                    "To modify the setup use the edit commands.")
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_1(self):

        """Tests setting up a draft with invalid input for player count."""

        logic = DraftSetupLogic()
        actual = logic.setup_draft("-1", "45")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_2(self):

        """Tests setting up a draft with invalid input for pick count."""

        logic = DraftSetupLogic()
        actual = logic.setup_draft("5", "1000")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_3(self):

        """Tests setting up a draft with invalid input for player count."""

        logic = DraftSetupLogic()
        actual = logic.setup_draft("wwwwww", "45")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_invalid_input_4(self):

        """Tests setting up a draft with invalid input for pick count."""

        logic = DraftSetupLogic()
        actual = logic.setup_draft("5", "ergd")
        expected = "Invalid parameters. Please use the '!help setup' command for details."
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_1(self):

        """Tests valid setup and checking return value."""

        logic = DraftSetupLogic()
        actual = logic.setup_draft("5", "50")
        expected = ("The draft has been set up. We have 5 players and 50 " +
                    "picks. Use the !join command to be added to the draft.")
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_2(self):

        """Tests valid setup and checking player count"""

        logic = DraftSetupLogic()
        logic.setup_draft("5", "50")
        actual = logic.player_count
        expected = 5
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_3(self):

        """Tests valid setup and checking pick count"""

        logic = DraftSetupLogic()
        logic.setup_draft("5", "50")
        actual = logic.pick_count
        expected = 50
        self.assertEqual(actual, expected)

    def test_setup_draft_valid_4(self):

        """Tests valid setup and checking setup value"""

        logic = DraftSetupLogic()
        logic.setup_draft("5", "50")
        actual = logic.setup
        expected = True
        self.assertEqual(actual, expected)

    #####################################
    ###       EDIT PLAYER TESTS       ###
    #####################################

    def test_edit_player_already_fired(self):

        """Tests editing a draft when it has already fire."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.fire_draft()
        actual = logic.edit_player("6")
        expected = "The draft has already fired. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_player_draft_not_setup(self):

        """Tests editing players when draft has not been set up."""

        logic = DraftSetupLogic()
        actual = logic.edit_player("5")
        expected = "The draft has not been set up. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_1(self):

        """Tests editing a draft with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_player("wwww")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_2(self):

        """Tests editing player count with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_player("456778")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_invalid_input_3(self):

        """Tests editing player count with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_player("-66")
        expected = "Invalid parameters. Please use the '!help edit_player' command for details."
        self.assertEqual(actual, expected)

    def test_edit_player_valid_1(self):

        """Tests editing a draft with valid input for pick count"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_player("5")
        expected = "Player count is: 5"
        self.assertEqual(actual, expected)

    def test_edit_player_valid_2(self):

        """Tests editing a draft with valid input for player count"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        logic.edit_player("5")
        actual = logic.player_count
        expected = 5
        self.assertEqual(actual, expected)

    def test_edit__player_too_small(self):

        """Tests editing a draft with valid input for player
        count but is smaller than the current number of
        players in the draft queue. """

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
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

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("player1", "1")
        logic.join_draft("player2", "2")
        logic.fire_draft()
        actual = logic.edit_pick("6")
        expected = "The draft has already fired. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_pick_draft_not_setup(self):

        """Tests editing players when draft has not been set up."""

        logic = DraftSetupLogic()
        actual = logic.edit_pick("5")
        expected = "The draft has not been set up. It cannot be edited."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_1(self):

        """Tests editing a draft with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_pick("wwww")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_2(self):

        """Tests editing player count with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_pick("456778")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_invalid_input_3(self):

        """Tests editing pick count with invalid input"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_pick("-66")
        expected = "Invalid parameters. Please use the '!help edit_pick' command for details."
        self.assertEqual(actual, expected)

    def test_edit_pick_valid_1(self):

        """Tests editing a draft with valid input for pick count"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        actual = logic.edit_pick("50")
        expected = "Pick count is: 50"
        self.assertEqual(actual, expected)

    def test_edit_pick_valid_2(self):

        """Tests editing a draft with valid input for player count"""

        logic = DraftSetupLogic()
        logic.setup_draft("4", "45")
        logic.edit_pick("50")
        actual = logic.pick_count
        expected = 50
        self.assertEqual(actual, expected)

    #####################################
    ###           RESET TESTS         ###
    #####################################

    def test_reset(self):

        """Tests the reset method once a draft is finished."""

        logic = DraftSetupLogic()
        logic.setup_draft("2", "45")
        logic.join_draft("p1", "1")
        logic.join_draft("p2", "2")
        logic.fire_draft()

        self.assertTrue(logic.draft_fired is True
                        and logic.setup is True
                        and logic.player_count == 2
                        and logic.pick_count == 45
                        and logic.players == {"1": "p1", "2": "p2"})

        logic.reset()

        self.assertTrue(logic.draft_fired is False
                        and logic.setup is False
                        and logic.player_count == 0
                        and logic.pick_count == 0
                        and logic.players == {})


if __name__ == "__main__":
    unittest.main()
