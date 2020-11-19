This is a Python hangman game project by Jan Grottel, started 14.11.2020.

Parameters:
Write a basic hangman game played on the command line.

Elements that will be needed:
1. Generate a random word to guess.
2. Implement a guessing game element.
3. Implement a graphic to represent the scaffold.
4. Implement basic UI elements - remaining guesses, letters used so far, the puzzle lookup.
5. Check for repeating letters (You already guessed 'X'!)
6. Victory, defeat screen.
7. Testing module - test the functions of the game if possible.
8. Any additional features are deemed unnecessary feature bloat at this point.

Things to learn:
1. Importing an element from a website.
2. Designing the program first using functions and pass statements. (pseudocode)
3. Building the test functions second.
4. Coding third.
5. Commenting on code while coding.

Post-mortem:

Unexpected things learned:
1. It's hard to design without coding automatically. When a function was created I wrote the code right away when it as simple.
2. Majority of the testing function was done at the very end. It tests only the two internal functions of generating a password and performing guesses.
3. Generating a unique password that is an actual word takes a lot of time.
4. Game probably needs a hard quit option (like writing 'QQ' as a guess)
5. Game could use a definition of the word as hint or at the end.
6. Global variables in this context were new to me.
7. Uncertain if the use of HangmanGame object was needed, but it was a good refresher.
8. Order and style of the end file is questionable.
9. Commenting your code is hard, but I tried to provide at least glimpses of what it was supposed to do.
10. 'requests' had these problems:
a) At the first website it returned 412 Precondition Failed, had to switch
b) second website had scripting and the words couldn't be scraped from the body
c) I like the use of 200 vs 404 code for checking validity of a word in the dictionary
11. When printing in the HangmanGame.guess() function it printed in the tests, which I didn't like, so I deleted that element. It was a 'Correct!/Incorrect!' message, that would be useful to the user. Implement these in the main functions, but not in the object.