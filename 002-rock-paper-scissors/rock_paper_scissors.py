from enum import Enum
from PIL import ImageTk, Image
import random
from tkinter import messagebox
import tkinter as tk


# Define data types for rock, paper, scissors and outcomes.
class Choice(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class Outcome(Enum):
    UNDETERMINED = 0
    PLAYER1_WIN = "beats"
    PLAYER2_WIN = "loses to"
    DRAW = "draws"


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


def mode():
    """
    Switch between 1P and 2P modes.
    Executed at startup and when mode button is pushed
    """
    mode_selected = messagebox.askquestion(
        "Mode selection",
        "Game supports two modes:\n\n\n"
        "YES: Singleplayer vs a random AI\n\n"
        "NO: Hotseat Multiplayer"
        )
    if mode_selected == "yes":
        p2.isAI = True
    else:
        p2.isAI = False
    mid.setup_mid_frame()
    p2.setup_frame()


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
        self.isAI = False
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

        if self.isAI:
            AI_choice = random.choice([self.rock, self.paper, self.scissors])
            AI_choice()

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
            game()

    def paper(self, _event=None):
        if not self.choice:
            self.choice_made()
            self.choice = Choice.PAPER
            game()

    def scissors(self, _event=None):
        if not self.choice:
            self.choice_made()
            self.choice = Choice.SCISSORS
            game()


class MiddleScreen(tk.LabelFrame):
    """
    Class governing the middle section of the screen.
    Contains the instructions, last result, record of previous results, quit
    reset and single/multiplayer menu buttons.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.results_so_far = []
        self.setup_mid_frame()

    def setup_mid_frame(self):
        """
        This function defines a start position for a game, a hard reset on the
        game record.
        Resets the tally of previous results.
        Puts the widgets in the frame.
        """
        self.results_so_far.clear()

        # Setup widgets
        # Instructions
        self.game_instruction = tk.Label(
            self,
            text="Rock, Paper or Scissors\n\n"
            "Choose using:\n"
            "> Buttons under images\n"
            "> Keyboard shortcuts!"
            )
        self.game_instruction.grid(row=0, column=0, columnspan=3)

        # Last Game
        self.last_game = tk.Label(self, text="Last Game:")
        self.last_game.grid(row=1, column=1, pady=10)

        self.last_game_p1 = tk.Label(self, text=" "*15)
        self.last_game_p1.grid_forget()
        self.last_game_p1.grid(row=2, column=0, pady=10)

        self.last_game_p2 = tk.Label(self, text=" "*15)
        self.last_game_p2.grid_forget()
        self.last_game_p2.grid(row=2, column=2, pady=10)

        self.last_result = tk.Label(self, text=" "*15)
        self.last_result.grid_forget()
        self.last_result.grid(row=2, column=1, pady=10)

        # Record so far
        self.this_session = tk.Label(self, text="This Session:")
        self.this_session.grid(row=3, column=1, pady=10)

        self.wins_p1 = tk.Label(self, text="0 won")
        self.wins_p1.grid_forget()
        self.wins_p1.grid(row=4, column=0, pady=10)

        self.wins_p2 = tk.Label(self, text="0 won")
        self.wins_p2.grid_forget()
        self.wins_p2.grid(row=4, column=2, pady=10)

        self.draws = tk.Label(self, text="0 draws")
        self.draws.grid_forget()
        self.draws.grid(row=4, column=1, pady=10)

        # Single/multiplayer button
        self.mode_button = tk.Button(self, text="Mode", command=mode)
        self.mode_button.grid(row=5, column=0, pady=50)
        # Reset record button
        self.reset_button = tk.Button(
            self, text="Reset", command=self.setup_mid_frame
            )
        self.reset_button.grid(row=5, column=1, pady=50)
        # Quit Button
        self.quit_button = tk.Button(self, text="Quit", command=root.quit)
        self.quit_button.grid(row=5, column=2, pady=50)

    def game_happened(self, p1, p2, result):
        """ Updates the frame to account for the last game played. """

        # Add the latest result to the list
        self.results_so_far.append(result)

        # Update the Labels
        self.last_game_p1.grid_forget()
        self.last_game_p1 = tk.Label(self, text=p1.value)
        self.last_game_p1.grid(row=2, column=0, pady=10)
        self.last_game_p2.grid_forget()
        self.last_game_p2 = tk.Label(self, text=p2.value)
        self.last_game_p2.grid(row=2, column=2, pady=10)
        self.last_result.grid_forget()
        self.last_result = tk.Label(self, text=result.value)
        self.last_result.grid(row=2, column=1, pady=10)

        self.wins_p1.grid_forget()
        self.wins_p1 = tk.Label(
            self, text=f"{self.results_so_far.count(Outcome.PLAYER1_WIN)} won"
            )
        self.wins_p1.grid(row=4, column=0, pady=10)
        self.wins_p2.grid_forget()
        self.wins_p2 = tk.Label(
            self, text=f"{self.results_so_far.count(Outcome.PLAYER2_WIN)} won"
            )
        self.wins_p2.grid(row=4, column=2, pady=10)
        self.draws.grid_forget()
        self.draws = tk.Label(
            self, text=f"{self.results_so_far.count(Outcome.DRAW)} draws"
            )
        self.draws.grid(row=4, column=1, pady=10)


# Main Game Window
root = tk.Tk()
root.title("Rock, Paper, Scissors!")
root.iconbitmap("002-rock-paper-scissors/resources/game.ico")
root.geometry("800x400")  # 300 200 300

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
p1.grid(row=0, column=0)

p2 = PlayerWindow(p2_shortcuts, root, text="Player 2", width=300, height=400)
p2.grid(row=0, column=2)

mid = MiddleScreen(root, text="Tally", width=200, height=355)
mid.grid(row=0, column=1)


def game():
    """
    After any button is pushed, tries to execute a game or RPS
    """
    if p1.choice and p2.choice:
        result = rock_paper_scissors(p1.choice, p2.choice)
        mid.game_happened(p1.choice, p2.choice, result)
        p1.setup_frame()
        p2.setup_frame()


def main():
    mode()
    root.mainloop()


if __name__ == '__main__':
    main()
