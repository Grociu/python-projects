import unittest
import hangman
import requests


# names of used functions can be changed here:
password = hangman.password


class TestPassword(unittest.TestCase):

    def test_password_given(self):
        """ 
        Test if the password function works properly for a normal input
        """
        self.assertEqual(password("dolphin"), "dolphin")

    def test_password_sanitation(self):
        """ 
        Test if the password function works properly for an improper input
        """
        self.assertNotEqual(password("hunter1"), "hunter1")
        self.assertNotEqual(password("Chit-Chat"), "chit-chat")
        self.assertNotEqual(password("@@@444"), "@@@444")

    def test_password_is_a_valid_word(self):
        """
        Tests whether a randomly generated password is in the dictionary.
        """
        word = password()
        dc_url = "https://www.dictionary.com/browse/" + word
        dc_page = requests.get(dc_url)
        self.assertEqual(dc_page.status_code, 200)

class HangmanClassSingleGuessTests(unittest.TestCase):
    
    def setUp(self):
        self.H = hangman.HangmanGame("dolphin")
        self.H.guess("a")

    def test_guess_appends_already_guessed(self):
        self.assertEqual(self.H.already_guessed, ["A"])
    def test_incorrect_guess_increments_wrong_guesses(self):
        self.assertEqual(self.H.wrong_guesses, 1)
    def test_gallows_is_incremented_correctly(self):
        self.assertEqual(self.H.gallows, ["O", " ", " ", " ", " ", " "])
    def test_game_not_won_after_one_guess(self):
        self.assertIs(self.H.game_won, False)
    def test_game_still_in_progress(self):
        self.assertIs(self.H.game_in_progress, True)

class HangmanClassMultipleGuessTests(unittest.TestCase):
    
    def setUp(self):
        self.H = hangman.HangmanGame("dolphin")
        self.H.guess("d")
        self.H.guess("o")
        self.H.guess("l")
        self.H.guess("p")
        self.H.guess("h")
        self.H.guess("i")

    def test_guess_appends_multiple(self):
        self.assertEqual(self.H.already_guessed, ["D", "O", "L", "P", "H", "I"])
    def test_incorrect_guess_is_not_incremented(self):
        self.assertEqual(self.H.wrong_guesses, 0)
    def test_gallows_is_not_changed(self):
        self.assertEqual(self.H.gallows, [" ", " ", " ", " ", " ", " "])
    def test_game_not_yet_won(self):
        self.assertIs(self.H.game_won, False)
    def test_game_still_in_progress_2(self):
        self.assertIs(self.H.game_in_progress, True)

class HangmanClassGameWinTests(unittest.TestCase):

    def setUp(self):
        self.H = hangman.HangmanGame("ace")
        self.H.guess("a")
        self.H.guess("c")
        self.H.guess("e")

    def test_game_won(self):
        self.assertIs(self.H.game_won, True)
    def test_game_no_longer_in_progress(self):
        self.assertIs(self.H.game_in_progress, False)

class HangmanClassGameLossTests(unittest.TestCase):

    def setUp(self):
        self.H = hangman.HangmanGame("dunce")
        self.H.guess("x")
        self.H.guess("z")
        self.H.guess("q")
        self.H.guess("k")
        self.H.guess("j")
        self.H.guess("y")

    def test_game_loss(self):
        self.assertIs(self.H.game_won, False)
    def test_game_no_longer_in_progress_2(self):
        self.assertIs(self.H.game_in_progress, False)
    def test_gallows_for_loss(self):
        self.assertEqual(self.H.gallows, ["O", "|", "/", "\\", "/", "\\"])



if __name__ == '__main__':
    unittest.main()
