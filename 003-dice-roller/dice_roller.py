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
        self.name = f"d{sides}"

    def roll(self):
        self.result = random.randint(1, self.sides)


class DicePool(object):
    """
    Class that represents a collection of dice objects.

    Attributes:
        .pool - a list of Dice objects in the DicePool
        .counter - a dictionary with a specific count of each die

    Methods:
        add() - adds a die to DicePool
        repr() - represents the DicePool as a string
    """
    def __init__(self):
        self.pool = []
        self.counter = dict()
        self.order = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]

    def add(self, die):
        """
        Adds a Dice object to .pool, updates .counter
        """
        if isinstance(die, Dice):
            self.pool.append(die)
            if die.name in self.counter:
                self.counter[die.name] += 1
            else:
                self.counter[die.name] = 1

    def __repr__(self):
        """ This also orders the dice in ascending order """
        return "  ".join(
            f"{self.counter[name]}{name}"
            for name in self.order
            if name in self.counter.keys()
            )


# Global Variable for the Dice Pool
dice_pool = DicePool()


# Functions
def add_die(sides):
    """ Adds a Dice(sides) object into  the dice pool to be rolled. """
    global dice_pool
    global dice_pool_window

    dice_pool.add(Dice(sides))

    dice_pool_window.grid_forget()
    dice_pool_window = tk.Label(
        root,
        background='white',
        text=repr(dice_pool)
        )
    dice_pool_window.grid(
        row=3, column=0, columnspan=7, ipady=30, padx=10, sticky='we'
        )


# Setup of tkinter
root = tk.Tk()
root.title("Dice roller!")
root.geometry("330x600")

# Label for adding dice
top_label = tk.Label(root, text="Add dice to the dicepool:")
top_label.grid(row=0, column=0, columnspan=7, padx=10, pady=10, sticky='w')

# Dice buttons
d4_button = tk.Button(root, text='d4', command=lambda: add_die(4))
d4_button.grid(row=1, column=0, padx=(20, 8))

d6_button = tk.Button(root, text='d6', command=lambda: add_die(6))
d6_button.grid(row=1, column=1, padx=8)

d8_button = tk.Button(root, text='d8', command=lambda: add_die(8))
d8_button.grid(row=1, column=2, padx=8)

d10_button = tk.Button(root, text='d10', command=lambda: add_die(10))
d10_button.grid(row=1, column=3, padx=8)

d12_button = tk.Button(root, text='d12', command=lambda: add_die(12))
d12_button.grid(row=1, column=4, padx=8)

d20_button = tk.Button(root, text='d20', command=lambda: add_die(20))
d20_button.grid(row=1, column=5, padx=8)

d100_button = tk.Button(root, text='d100', command=lambda: add_die(100))
d100_button.grid(row=1, column=6, padx=(8, 20))

# Label for adding dice
dice_pool_label = tk.Label(root, text="Current dicepool:")
dice_pool_label.grid(
    row=2, column=0, columnspan=7, padx=10, pady=10, sticky='w'
    )

# Dice pool window
dice_pool_window = tk.Label(root, background='white', text='empty')
dice_pool_window.grid(
    row=3, column=0, columnspan=7, padx=10, ipady=30, sticky='we'
    )

if __name__ == '__main__':
    root.mainloop()
