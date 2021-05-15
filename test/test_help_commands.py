from botBackend import help_commands
import unittest


class TestHelpCommands(unittest.TestCase):

    def test_help_draft_valid_empty(self):

        """Tests getting the default help message
        when no parameters are passed in."""

        command = "default"

        actual = help_commands.help_draft(command)
        expected = ("```I am DraftBot! I let you do custom rotisserie drafts.\n" +
                    "Here are my commands and their parameters:\n\n" +
                    "1. cancel\n" +
                    "    - Cancels the draft during setup if no one joined.\n\n"
                    "2. cancelprepick\n" +
                    "    - Allows the user to cancel a prepick.\n\n" +
                    "3. card\n" +
                    "    - Displays the image of the card provided it exists.\n\n" +
                    "4. edit_format\n" +
                    "    - Edit the format of the draft during setup.\n\n" +
                    "5. edit_pick\n" +
                    "    - Edit number of picks in the draft during setup.\n\n" +
                    "6. edit_player\n" +
                    "    - Edit number of players in the draft during setup.\n\n" +
                    "7. fire\n" +
                    "    - Fires the draft once setup is complete.\n\n" +
                    "8. getprepicks\n" +
                    "    - Allows the user to get a list of their prepicks.\n\n"
                    "9. help\n" +
                    "    - Displays the helpful message you are currently seeing.\n\n" +
                    "10. info\n" +
                    "    - Displays information on the setup of the draft.\n\n" +
                    "11. join\n" +
                    "    - Allows a user to join a draft.\n\n" +
                    "12. leave\n" +
                    "    - Allows a user to leave the draft during the setup\n" +
                    "      stage.\n\n" +
                    "13. legal\n" +
                    "    - States the legality of a card.\n\n" +
                    "14. pick\n" +
                    "    - Allows a user to pick a card during the draft.\n\n" +
                    "15. prepick\n" +
                    "    - Allows the user to prepick a card.\n\n" +
                    "16. remind\n" +
                    "    - Reminds a user to pick a card when the draft\n" +
                    "      has fired and is running.\n\n" +
                    "17. setup\n" +
                    "    - Sets up a draft with a specified player and pick count.\n\n" +
                    "Type !help {command} for more info on a command.```")

        self.assertEqual(actual, expected)

    def test_help_draft_valid_parameter(self):

        """Tests getting the info message when that
        parameter is passed in."""

        command = "info"

        actual = help_commands.help_draft(command)
        expected = ("```\n" +
                    "info\n\n" +
                    "This displays information on the setup of the draft.\n\n" +
                    "    example: !info\n" +
                    "    - Displays the setup of the draft before it fires.```")

        self.assertEqual(actual, expected)

    def test_help_draft_invalid_1(self):

        "Tests getting an invalid command."

        command = "this is not valid"
        actual = help_commands.help_draft(command)
        expected = "No command found."
        self.assertEqual(actual, expected)

    def test_help_draft_invalid_2(self):

        """Tests getting an invalid command."""

        command = "edit invalid"
        actual = help_commands.help_draft(command)
        expected = "No command found."
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
