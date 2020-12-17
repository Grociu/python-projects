import dice_roller
import unittest


# function definitions
add_die = dice_roller.add_die
reset = dice_roller.reset
execute = dice_roller.execute


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

    def test_correct_repr_after_adding_one(self):
        self.assertEqual(
            dice_roller.dice_pool_window['text'],
            '1d4'
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
        self.assertEqual(
            dice_roller.dice_pool_window['text'],
            '1d4  1d6'
        )

    def test_if_dice_unrolled(self):
        for die in dice_roller.dice_pool.pool:
            self.assertEqual(die.result, 0)

    def tearDown(self):
        dice_roller.dice_pool.empty()


class TestReset(unittest.TestCase):

    def setUp(self):
        dice_roller.dice_pool = dice_roller.DicePool()
        add_die(4)
        add_die(4)
        add_die(10)
        add_die(12)
        reset()

    def test_if_pool_is_empty(self):
        self.assertEqual(dice_roller.dice_pool.pool, [])

    def test_if_counter_is_empty(self):
        self.assertEqual(dice_roller.dice_pool.counter, dict())

    def test_the_output_text(self):
        self.assertEqual(
            dice_roller.dice_pool_window['text'],
            'empty'
        )


class TestExecute(unittest.TestCase):

    def setUp(self):
        dice_roller.dice_pool = dice_roller.DicePool()

    def without_new_dice_text_does_not_change(self):
        initial_text = dice_roller.result_window['text']
        execute()
        self.assertEqual(
            dice_roller.result_window['text'],
            initial_text)

    def dice_pool_does_not_change(self):
        add_die(4)
        add_die(6)
        initial_dice_pool = dice_roller.dice_pool.pool
        execute()
        self.assertEqual(
            dice_roller.dice_pool.pool,
            initial_dice_pool)

    def dice_are_rolled(self):
        add_die(100)
        add_die(100)
        execute()
        for die in dice_roller.dice_pool.pool:
            self.assertNotEqual(
                die.result,
                0
            )

    def test_correct_output_text(self):
        add_die(4)
        add_die(4)
        add_die(6)
        execute()
        d4_results = [
            dice_roller.dice_pool.pool[0].result,
            dice_roller.dice_pool.pool[1].result
        ]
        d4_results.sort()
        d6_results = [
            dice_roller.dice_pool.pool[2].result
        ]
        total_sum = sum(d4_results) + d6_results[0]
        target_text = (
            f"2d4: {d4_results}, Sum: {sum(d4_results)}\n"
            f"1d6: {d6_results}, Sum: {d6_results[0]}\n"
            f"\nTotal Sum: {total_sum}"
        )
        self.assertEqual(
            dice_roller.result_window['text'],
            target_text
        )


if __name__ == '__main__':
    unittest.main()
