import requests
import bs4


def is_in_dictionary(word):
    """
    Checks whether a given word (string) is in the dictionary, by requesting it
    from the dictionary.com website and checking for the 200 code.
    """
    dc_url = "https://www.dictionary.com/browse/" + word.lower()
    dc_page = requests.get(dc_url)
    return dc_page.status_code == 200


def password(word=""):
    """
    Returns the word (string) given as argument or a random word from the
    randoword.com website using requests and BeautifulSoup.
    """
    if word and word.isalpha() and is_in_dictionary(word):
        return word
    else:
        while not word.isalpha() or not is_in_dictionary(word):
            rw_url = "https://randomword.com/"
            rw_page = requests.get(rw_url)
            rw_soup = bs4.BeautifulSoup(rw_page.content, "html.parser")
            word = rw_soup.find("div", id="random_word").text
        return word


class HangmanGame():
    """
    A single game instance of Hangman
    """

    def __init__(self, word=""):
        self.password = password(word).upper()
        self.already_guessed = []
        self.wrong_guesses = 0
        self.game_in_progress = True
        self.game_won = False
        self.gallows = [" "]*6
        self.body = ["O", "|", "/", "\\", "/", "\\"]

    def guess(self, letter):
        """
        Performs a guess using a given letter (char).
        Input will be a unique letter character not tried before in the current
        game.
        """
        letter = letter.upper()
        self.already_guessed.append(letter)
        if letter not in [char for char in self.password]:
            self.gallows[self.wrong_guesses] = self.body[self.wrong_guesses]
            self.wrong_guesses += 1
            self.check_for_loss()
        else:
            self.check_for_victory()

    def draw_gallows(self):
        """
        Draws the gallows, using current game state.
        """
        print(
            f"\n"
            f"     ___________\n"
            f"     |         |\n"
            f"     |         {self.gallows[0]}\n"
            f"     |        {self.gallows[2]}{self.gallows[1]}{self.gallows[3]}\n"
            f"     |        {self.gallows[4]} {self.gallows[5]}\n"
            f"     |"
            f"\n"
            )

    def draw_the_password(self):
        """
        Draws the password with the current guesses and undersores for blank
        letters.
        """
        print("\n")
        print(
            " ".join(
                char
                if char in self.already_guessed
                else "_"
                for char in self.password
                )
        )
        print("\n")

    def draw_stats(self):
        """
        Draws the current stats - already guessed letters, number of fails
        remaining etc.
        """
        print(
            f"\n"
            f"You already tried these: {self.already_guessed}.\n"
            f"You can only fail {5 - self.wrong_guesses} more time(s).\n"
            f"\n"
        )

    def check_for_victory(self):
        """
        Checks if the player won the game.
        """
        if set(
            char for char in self.password
        ).issubset(set(self.already_guessed)):
            self.game_won = True
            self.game_in_progress = False

    def check_for_loss(self):
        """
        Checks if the player lost the game.
        """
        if self.wrong_guesses >= 6:
            self.game_in_progress = False


def greeting():
    print("Welcome to Hangman!")
    name_choice()


def name_choice():
    global player_name
    player_name = input("Enter your name: ")
    main_menu()


def main_menu():
    global player_name
    choice = ""
    print(
        f"{player_name} choose your option: "
        "(N)ew game, (C)hange player name, (Q)uit."
        )
    while choice not in {'n', 'c', 'q'}:
        choice = input("Choice: ")
        choice = choice.lower()
    if choice == "q":
        goodbye()
    if choice == "c":
        name_choice()
    if choice == "n":
        game()


def goodbye():
    global player_name
    print(f"Thanks for playing {player_name}!")


def game():
    """
    Main game function. Creates an object that is a game of Hangman,
    and asks for guesses while the game is active.
    """

    Game = HangmanGame()

    while Game.game_in_progress:
        guess = ""  # Clear the guess variable before next round
        Game.draw_gallows()
        Game.draw_the_password()
        Game.draw_stats()
        while (
            not guess.isalpha()  # has to be a letter
            or len(guess) != 1  # has to be a single char
            or guess in Game.already_guessed  # has to be a unique char
        ):
            guess = input("Guess a letter in the magic word: ")
        Game.guess(guess)

    if Game.game_won:
        print(f"Victory! The word was:   {Game.password}")
    else:
        print("Defeat!")
        Game.draw_gallows
        print(f"The word was:   {Game.password}")

    main_menu()


def main():
    greeting()


if __name__ == '__main__':
    main()
