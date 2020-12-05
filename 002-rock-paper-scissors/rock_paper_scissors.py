import tkinter as tk
from enum import Enum
import random


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

def main():
    pass

if __name__ == '__main__':
    main()