from botBackend import scryfallapi
import unittest

class TestRemindPicks(unittest.TestCase):

    def test_card_image_exists_true_1(self):

        """Tests getting the image of a valid card."""    

        card = ('lightning', 'bolt')
        actual = scryfallapi.get_card_image(card)[1]
        expected = "https://c1.scryfall.com/file/scryfall-cards/normal/front/c/e/ce711943-c1a1-43a0-8b89-8d169cfb8e06.jpg?1601078281"
        self.assertEqual(actual, expected)

    def test_card_image_exists_true_2(self):
        
        """Tests getting the name of a valid card."""    
        
        card = ('lightnng', 'bolt')
        actual = scryfallapi.get_card_image(card)[0]
        expected = "Lightning Bolt"
        self.assertEqual(actual, expected)

    def test_card_image_exists_false_1(self):
        
        """Tests getting the image of a invalid card."""  

        card = ('"fghjkliuytr')
        with self.assertRaises(ValueError):
            actual = scryfallapi.get_card_image(card)[1]

    def test_card_image_exists_false_2(self):
        
        """Tests getting the name of a invalid card."""  
        
        card = ('"fghjkliuytr')
        with self.assertRaises(ValueError):
            actual = scryfallapi.get_card_image(card)[0]

    def test_format_legal_exists_true_1(self):
        
        """Tests getting the legality of a valid card."""  

        card = ('lightning', 'bolt')
        actual = scryfallapi.get_card_legality(card)[1]
        expected = {'standard': 'not_legal', 'future': 'not_legal', 
                    'historic': 'not_legal', 'gladiator': 'not_legal', 
                    'pioneer': 'not_legal', 'modern': 'legal', 
                    'legacy': 'legal', 'pauper': 'legal', 'vintage': 'legal', 
                    'penny': 'not_legal', 'commander': 'legal', 'brawl': 
                    'not_legal', 'duel': 'legal', 'oldschool': 'not_legal', 
                    'premodern': 'legal'}

        self.assertEqual(actual, expected)

    def test_format_legal_exists_true_2(self):
        
        """Tests getting the name of a valid card."""  
        
        card = ('lightnng', 'bolt')
        actual = scryfallapi.get_card_legality(card)[0]
        expected = "Lightning Bolt"
        self.assertEqual(actual, expected)

    def test_format_legal_exists_false_1(self):
        
        """Tests getting the legality of a invalid card."""  

        card = ('aesrfdg', 'bolt')
        with self.assertRaises(ValueError):
            actual = scryfallapi.get_card_legality(card)[1]

    def test_format_legal_exists_false_2(self):
        
        """Tests getting the legality of a invalid card.""" 

        card = ('esrfdgfh', 'bolt')
        with self.assertRaises(ValueError):
            actual = scryfallapi.get_card_legality(card)[0]

    def test_card_exists_true(self):
        
        card = ('lightning', 'bolt')
        self.assertTrue(scryfallapi.card_exists(card))
  
    def test_card_exists_false(self):
        
        card = ('waesrdgfh', 'bolt')
        self.assertFalse(scryfallapi.card_exists(card))

    def test_fuzzied_correct(self):
        
        card = ('lightnang', 'bolt')
        actual = scryfallapi.card_exists(card)
        expected = True
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()