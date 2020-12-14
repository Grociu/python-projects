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


# Global Variable for the Dice Pool
dice_pool = []


# Functions
def add_die(sides):
    """ Adds a Dice(sides) object into  the dice pool to be rolled. """
    pass


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

if __name__ == '__main__':
    root.mainloop()
