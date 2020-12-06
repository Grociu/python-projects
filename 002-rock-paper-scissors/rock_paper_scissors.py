import tkinter as tk
import random
from enum import Enum
from PIL import ImageTk, Image


# Define data types for rock, paper, scissors and outcomes.
class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Outcome(Enum):
    UNDETERMINED = 0
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


def p1_rock():
    global p1_choice

    p1_made_choice()
    p1_choice = Choice.ROCK
    pass


def p1_paper():
    global p1_choice

    p1_made_choice()
    p1_choice = Choice.PAPER
    pass


def p1_scissors():
    p1_made_choice()
    p1_choice = Choice.SCISSORS
    pass

def p1_made_choice():
    """ Player 1 made a choice.
    Disables buttons. 
    Displays a message if waiting for player 2 choice. (?)
    Display game result if both made choice. (?)
    """
    global p1_rock_button
    global p1_paper_button
    global p1_scissors_button
    global p1_choice_label

    p1_rock_button = tk.Button(
        p1_frame, text="rock (Q)", command=p1_rock, state="disabled"
        )
    p1_rock_button.grid(row=2, column=0)

    p1_paper_button = tk.Button(
        p1_frame, text="paper (W)", command=p1_paper, state="disabled"
        )
    p1_paper_button.grid(row=2, column=2)

    p1_scissors_button = tk.Button(
        p1_frame, text="scissors (A)", command=p1_scissors, state="disabled"
        )
    p1_scissors_button.grid(row=4, column=1)

    p1_choice_label.grid_forget()
    p1_choice_label = tk.Label(p1_frame, text="P1 has chosen!")
    p1_choice_label.grid(row=5, column=1, pady=30)


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

# Player One Game Box
p1_frame = tk.LabelFrame(root, text="Player 1", width=300, height=400)
p1_frame.grid(row=0, column=0)

p1_rock_picture = tk.Label(p1_frame, image=rock_img)
p1_rock_picture.grid(row=1, column=0)
p1_rock_button = tk.Button(p1_frame, text="rock (Q)", command=p1_rock)
p1_rock_button.grid(row=2, column=0)

p1_paper_picture = tk.Label(p1_frame, image=paper_img)
p1_paper_picture.grid(row=1, column=2)
p1_paper_button = tk.Button(p1_frame, text="paper (W)", command=p1_paper)
p1_paper_button.grid(row=2, column=2)

p1_scissors_picture = tk.Label(p1_frame, image=scissors_img)
p1_scissors_picture.grid(row=3, column=1)
p1_scissors_button = tk.Button(p1_frame, text="scissors (A)", command=p1_scissors)
p1_scissors_button.grid(row=4, column=1)

p1_choice_label = tk.Label(p1_frame, text="No choice made")
p1_choice_label.grid(row=5, column=1, pady=30)

# Main Tkinter Loop
root.mainloop()

if __name__ == '__main__':
    main()