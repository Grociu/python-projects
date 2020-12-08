from enum import Enum
from PIL import ImageTk, Image
import random
import tkinter as tk


# Define data types for rock, paper, scissors and outcomes.
class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Outcome(Enum):
    UNDETERMINED = 1
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    DRAW = 3

def rock_paper_scissors(choice_player_1, choice_player_2):
    """
    Executes a game of Rock, Paper, Scissors on instances of Choice.
    Raises ValueError if input is incorrect.
    Returns instances of Outcome.
    """
    if not (
        isinstance(choice_player_1, Choice) and 
        isinstance(choice_player_2, Choice)
    ):
        raise TypeError("Invalid Input") 
    if choice_player_1 == choice_player_2:
        return Outcome.DRAW
    if (
        choice_player_1 == Choice.ROCK and choice_player_2 == Choice.SCISSORS
     ) or (
        choice_player_1 == Choice.SCISSORS and choice_player_2 == Choice.PAPER
     ) or (
        choice_player_1 == Choice.PAPER and choice_player_2 == Choice.ROCK
     ):
        return Outcome.PLAYER1_WIN
    else:
        return Outcome.PLAYER2_WIN


class PlayerWindow(tk.LabelFrame):

    def __init__(self, shortcuts, master, **kwargs):
        super().__init__(master, **kwargs)
        # Binds the keyboard keys to specific button functions
        master.bind(shortcuts[0], self.rock)
        master.bind(shortcuts[0].lower(), self.rock)
        master.bind(shortcuts[1], self.paper)
        master.bind(shortcuts[1].lower(), self.paper)
        master.bind(shortcuts[2], self.scissors)
        master.bind(shortcuts[2].lower(), self.scissors)
        self.shortcuts = shortcuts
        self.setup_frame()

    def setup_frame(self):
        """
        Sets up the frame at game start, ready to receive player input.
        """
        self.choice = None
        
        self.rock_picture = tk.Label(self, image=rock_img)
        self.rock_picture.grid(row=1, column=0)

        self.rock_button = tk.Button(
            self, text=f"rock ({self.shortcuts[0]})", command=self.rock,
            relief='sunken'
            )
        self.rock_button.grid(row=2, column=0)
        
        self.paper_picture = tk.Label(self, image=paper_img)
        self.paper_picture.grid(row=1, column=2)

        self.paper_button = tk.Button(
            self, text=f"paper ({self.shortcuts[1]})", command=self.paper,
            relief='sunken'
            )
        self.paper_button.grid(row=2, column=2)

        self.scissors_picture = tk.Label(self, image=scissors_img)
        self.scissors_picture.grid(row=3, column=1)
        
        self.scissors_button = tk.Button(
            self, text=f"scissors ({self.shortcuts[2]})",
            command=self.scissors, relief='sunken'
            )
        self.scissors_button.grid(row=4, column=1)

        self.choice_label = tk.Label(self, text="No choice made")
        self.choice_label.grid(row=5, column=1, pady=30)


    def choice_made(self):
        """
        Player pushed any button.
        Update the frames after any button is pushed, disables the buttons.
        """
        self.rock_button = tk.Button(
            self, text=f"rock ({self.shortcuts[0]})",
            relief='sunken', command=self.rock,
            state="disabled"
        )
        self.rock_button.grid(row=2, column=0)

        self.paper_button = tk.Button(
            self, text=f"paper ({self.shortcuts[1]})", 
             relief='sunken', command=self.paper,
            state="disabled"
        )
        self.paper_button.grid(row=2, column=2)

        self.scissors_button = tk.Button(
            self, text=f"scissors ({self.shortcuts[2]})",
            relief='sunken', command=self.scissors,
            state="disabled"
        )
        self.scissors_button.grid(row=4, column=1)

        self.choice_label.grid_forget()
        self.choice_label = tk.Label(self, text="Player has chosen!")
        self.choice_label.grid(row=5, column=1, pady=30)
    

    def rock(self, _event=None):  # _event=None is needed for the keybindings
        if not self.choice:
            self.choice_made()
            self.choice = Choice.ROCK


    def paper(self, _event=None):
        if not self.choice:
            self.choice_made()
            self.choice = Choice.PAPER


    def scissors(self, _event=None):
        if not self.choice:
            self.choice_made()
            self.choice = Choice.SCISSORS


def main():
    pass


# Main Game Window
root = tk.Tk()
root.title("Rock, Paper, Scissors!")
root.iconbitmap("002-rock-paper-scissors/resources/game.ico")
root.geometry("800x400") # 300 200 300

# Tkinter setup for images
rock_img = ImageTk.PhotoImage(
    Image.open("002-rock-paper-scissors/resources/rock.jpg")
    )
paper_img = ImageTk.PhotoImage(
    Image.open("002-rock-paper-scissors/resources/paper.jpg")
    )
scissors_img = ImageTk.PhotoImage(
    Image.open("002-rock-paper-scissors/resources/scissors.jpg")
    )

# Define keyboard shortcuts for P1 and P2
p1_shortcuts = ["Q", "W", "A"]
p2_shortcuts = ["O", "P", "L"]

# Setup the Game window
p1 = PlayerWindow(p1_shortcuts, root, text="Player 1", width=300, height=400)
p1.grid(row=1, column=1)

p2 = PlayerWindow(p2_shortcuts, root, text="Player 2", width=300, height=400)
p2.grid(row=1, column=2)

# Main Tkinter Loop
root.mainloop()

if __name__ == '__main__':
    main()