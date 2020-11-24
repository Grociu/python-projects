import unittest
import rock_paper_scissors


# functions used
rps = rock_paper_scissors.rock_paper_scissors
placeholder = None #change this to the correct types

class TestRPS(unittest.TestCase):

    # tests for correct input
    def test_string_input(self):
        "A string should raise an error"
        self.assertRaises(rps("scissors","rock"), TypeError)

    def test_partial_string_input(self):
        "A string should raise an error"
        self.assertRaises(rps(placeholder,"rock"), TypeError)

    def test_integer_input(self):
        "A string should raise an error"
        self.assertRaises(rps(1,0), TypeError)

    def test_boolean_input(self):
        "A string should raise an error"
        self.assertRaises(rps(True, False), TypeError)


    # tests for correct outcomes
    def test_rps_outcome_1_pp(self):
        """ Paper Paper """
        pass
    def test_rps_outcome_2_ps(self):
        """ Paper Scissors """
        pass
    def test_rps_outcome_3_pr(self):
        """ Paper Rock """
        pass
    def test_rps_outcome_4_ss(self):
        """ Scissors Scissors """
        pass
    def test_rps_outcome_5_sp(self):
        """ Scissors Paper """
        pass
    def test_rps_outcome_6_sr(self):
        """ Scissors Rock """
        pass
    def test_rps_outcome_7_rr(self):
        """ Rock Rock """
        pass
    def test_rps_outcome_8_rp(self):
        """ Rock Paper """
        pass
    def test_rps_outcome_9_rs(self):
        """ Rock Scissors """
        pass


if __name__ == '__main__':
    unittest.main()