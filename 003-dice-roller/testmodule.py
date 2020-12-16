import dice_roller
import unittest


# function definitions
add_die = dice_roller.add_die


class TestAddDie(unittest.TestCase):

    def setUp(self):
        dice_roller.dice_pool = dice_roller.DicePool()
        add_die(4)

    def test_something_is_added(self):
        self.assertFalse(dice_roller.dice_pool.pool == [])

    def test_if_element_is_a_dice_object(self):
        self.assertIsInstance(
            dice_roller.dice_pool.pool[0],
            dice_roller.Dice
        )

    def test_only_one_element_is_in(self):
        self.assertEqual(
            len(dice_roller.dice_pool.pool),
            1
        )

    def test_correct_name_of_die(self):
        self.assertEqual(
            dice_roller.dice_pool.pool[0].name,
            "d4"
        )

    def test_adding_a_second_element(self):
        add_die(6)
        self.assertIsInstance(
            dice_roller.dice_pool.pool[1],
            dice_roller.Dice
        )
        self.assertEqual(
            len(dice_roller.dice_pool.pool),
            2
        )
        self.assertEqual(
            dice_roller.dice_pool.pool[1].name,
            "d6"
        )

    def test_if_dice_unrolled(self):
        for die in dice_roller.dice_pool.pool:
            self.assertEqual(die.result, 0)

    def tearDown(self):
        dice_roller.dice_pool.pool.clear()


if __name__ == '__main__':
    unittest.main()
