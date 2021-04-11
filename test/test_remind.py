from botBackend import remind
import unittest

class TestRemind(unittest.TestCase):

    #####################################
    ###       VALID DIGIT TESTS       ###
    #####################################

    def test_valid_time_hour_digit(self):
        """Tests valid time with valid hour"""

        self.assertTrue(remind.valid_time_input("0","0","0"))
    
    def test_invalid_time_hour_digit(self):    
        """Tests valid time with invalid hour"""
        
        self.assertFalse(remind.valid_time_input("W","0","0"))
    
    def test_valid_time_minute_digit(self):
        """Tests valid time with valid minute"""
        
        self.assertTrue(remind.valid_time_input("0","0","0"))
        
    def test_invalid_time_minute_digit(self):  
        """Tests valid time with invalid minute"""
        
        self.assertFalse(remind.valid_time_input("0","W","0"))
    
    def test_valid_time_second_digit(self):
        """Tests valid time with valid second"""
        
        self.assertTrue(remind.valid_time_input("0","0","0"))
        
    def test_invalid_time_second_digit(self):  
        """Tests valid time with invalid second"""
        
        self.assertFalse(remind.valid_time_input("0","0","W"))

    #####################################
    ###       VALID BOUNDS TESTS      ###
    #####################################

    def test_valid_time_hour_bounds(self):
        """Tests valid time with hour in bounds"""
        self.assertTrue(remind.valid_time_input("11","0","0"))

    def test_invalid_time_hour_upper_bound(self):
        """Tests invalid time with hour exceeding upper bound"""
        self.assertFalse(remind.valid_time_input("55","0","0"))

    def test_invalid_time_hour_lower_bound(self):
        """Tests invalid time with hour exceeding lower bound"""
        self.assertFalse(remind.valid_time_input("-55","0","0"))

    def test_valid_time_minute_valid_bounds(self):
        """Tests valid time with minute in bounds"""
        self.assertTrue(remind.valid_time_input("0","56","0"))

    def test_invalid_time_minute_upper_bound(self):
        """Tests invalid time with minute exceeding upper bound"""
        self.assertFalse(remind.valid_time_input("0","55555","0"))

    def test_invalid_time_minute_lower_bound(self):
        """Tests invalid time with minute exceeding lower bound"""
        self.assertFalse(remind.valid_time_input("-","-66","0"))

    def test_valid_time_second_valid_bounds(self):
        """Tests valid time with second in bounds"""
        self.assertTrue(remind.valid_time_input("0","0","54"))

    def test_invalid_time_second_upper_bound(self):
        """Tests invalid time with second exceeding upper bound"""
        self.assertFalse(remind.valid_time_input("0","0","55555"))

    def test_invalid_time_second_lower_bound(self):
        """Tests invalid time with second exceeding lower bound"""
        self.assertFalse(remind.valid_time_input("0","0","-88"))

    #####################################
    ###          NOTIFY TESTS         ###
    #####################################

    def test_notify_1(self):
        """Tests the confirmation print message"""

        actual = remind.notify("0", "0", "6")
        expected = "I will remind you in: 0 hours, 0 minutes, and 6 seconds."
        self.assertEqual(actual, expected)

    def test_notify_2(self):
        """Tests the confirmation print message"""

        actual = remind.notify("1", "1", "1")
        expected = "I will remind you in: 1 hour, 1 minute, and 1 second."
        self.assertEqual(actual, expected)

    def test_notify_3(self):
        """Tests the confirmation print message"""

        actual = remind.notify("0", "0", "0")
        expected = "I will remind you in: 0 hours, 0 minutes, and 0 seconds."
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()