import unittest
import rock_paper_scissors as r_p_s


# functions used
rps = r_p_s.rock_paper_scissors
Choice = r_p_s.Choice
Outcome = r_p_s.Outcome


class TestRPS(unittest.TestCase):

    # tests for correct input
    def test_string_input(self):
        """A string should raise an error"""
        self.assertRaises(TypeError, rps, "scissors", "rock")

    def test_partial_string_input(self):
        """A string should raise an error"""
        self.assertRaises(TypeError, rps, Choice.ROCK, "rock")

    def test_integer_input(self):
        """A string should raise an error"""
        self.assertRaises(TypeError, rps, 1, 0)

    def test_boolean_input(self):
        """A string should raise an error"""
        self.assertRaises(TypeError, rps, True, False)

    # tests for correct outcomes
    def test_rps_outcome_1_pp(self):
        """ Paper Paper """
        self.assertIs(rps(Choice.PAPER, Choice.PAPER), Outcome.DRAW)

    def test_rps_outcome_2_ps(self):
        """ Paper Scissors """
        self.assertIs(rps(Choice.PAPER, Choice.SCISSORS), Outcome.PLAYER2_WIN)

    def test_rps_outcome_3_pr(self):
        """ Paper Rock """
        self.assertIs(rps(Choice.PAPER, Choice.ROCK), Outcome.PLAYER1_WIN)

    def test_rps_outcome_4_ss(self):
        """ Scissors Scissors """
        self.assertIs(rps(Choice.SCISSORS, Choice.SCISSORS), Outcome.DRAW)

    def test_rps_outcome_5_sp(self):
        """ Scissors Paper """
        self.assertIs(rps(Choice.SCISSORS, Choice.PAPER), Outcome.PLAYER1_WIN)

    def test_rps_outcome_6_sr(self):
        """ Scissors Rock """
        self.assertIs(rps(Choice.SCISSORS, Choice.ROCK), Outcome.PLAYER2_WIN)

    def test_rps_outcome_7_rr(self):
        """ Rock Rock """
        self.assertIs(rps(Choice.ROCK, Choice.ROCK), Outcome.DRAW)

    def test_rps_outcome_8_rp(self):
        """ Rock Paper """
        self.assertIs(rps(Choice.ROCK, Choice.PAPER), Outcome.PLAYER2_WIN)

    def test_rps_outcome_9_rs(self):
        """ Rock Scissors """
        self.assertIs(rps(Choice.ROCK, Choice.SCISSORS), Outcome.PLAYER1_WIN)


if __name__ == '__main__':
    unittest.main()
