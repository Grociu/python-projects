import random
import tkinter as tk


class Dice(object):
    """
    A generic class for a die type object.
    Has a number of sides n, that defines high roll on a die
    Includes a roll method that returns a random value from 1 to n
    """

    def __init__(self, sides):
        self.sides = sides
        self.result = 0

    def roll(self):
        self.result = random.randint(1, self.sides)


class D4(Dice):
    """ A d4 """
    def __init__(self):
        super().__init__(4)


class D6(Dice):
    """ A d6 """
    def __init__(self):
        super().__init__(6)


class D8(Dice):
    """ A d8 """
    def __init__(self):
        super().__init__(8)


class D10(Dice):
    """ A d10 """
    def __init__(self):
        super().__init__(10)


class D12(Dice):
    """ A d12 """
    def __init__(self):
        super().__init__(12)


class D20(Dice):
    """ A d20 """
    def __init__(self):
        super().__init__(20)


class D100(Dice):
    """ A d100 """
    def __init__(self):
        super().__init__(100)


def main():
    pass


if __name__ == '__main__':
    main()
