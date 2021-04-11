from botBackend.draft_pick_logic import DraftPickLogic, CardTracker
import unittest
 
class TestDraftPickLogic(unittest.TestCase):
    
    def test_card_tracker_get_cards(self):
        
        players = ['p1', 'p2', 'p3', 'p4']

        card_tracker = CardTracker(players)

        card_tracker.add_card('p1', 'lightning bolt')
        card_tracker.add_card('p1', 'lightning bolt')

    def test_card_tracker_get_cardrs(self):
        pass


if __name__ == "__main__":
    unittest.main()