This is a python Dice Roller project by Jan Grottel. Started on 13.12.2020

Parameters:
Write a dice rolling app with a basic UI.

Elements that will be needed as of project start:
1. A tkinter interface for the user
2. Input box for the number of dice
3. Input box for type of dice (d4,d6,d8,d10,d20,d100)
4. An ability to define multiple rolls like 8d6 + 2d8 + d100 - Add button
5. Feedback to the user - choices so far
6. Execute button
7. A list of rolled results, maybe sorted by type and then from highest to lowest
8. Sum of all rolls and sum of each die type roll rolls
9. Reset button, Quit button
10. Instructions
11. Testing module - test the functions of the game if possible.
12. Any additional features are deemed unnecessary feature bloat at this point.

Things to learn:
1. tkinter input box, with input sanitation, error message (?)
2. tkinter dropdown menu
3. Basic GUI design
4. Designing the program using functions, classes and pass statements.
5. Building the test functions.
6. Coding.
7. Commenting on code while coding.

Post-mortem:
1. dice_pool started as a list, ended up being an object. It's likely
2. DicePool object could probably have more methods, like a method to generate a report, instead of this being handled by a top level function
3. Having top level functions and referring to global variables doesn't feel good, maybe make them an object?
4. The solution to the problem of sorting the dice_pool by dice value is hacky in my opinion.
    a) a dictionary cannot be sorted like a list
    b) I don't want all the items in the dictionary if there are no Dice of that type
    c) I created a constant, sorted list of dice names and iterate through them.
5. Tests were written after the functions were made. Not happy about that.
6. Dropdown menu was not needed, buttons work fine.

Unexpected things learned:
1. From the project 002 and the tkinter tutorial I was under the impression you have to grid_forget, redefine the widget, and place it on the grid again to update.
This was actually pretty annoying to me, and a google search revealed a more elegant way of achieving change of label text by refering to the window_name_label['text'] attribute
2. global variables are messy for unittesting
3. you can put a string in a parenthesis to make a multi line f-string for cleaner code
4. Tweaking the parameters of widgets to make it look acceptable is an absolute pain in the neck
5. Initial idea of having many different functions for each button was neatly solved by command=lambda: add_die(param). Studying and understanding the lambda expressions can be beneficial in the future.
6. ipady (internal padding) parameter was creating unneeded whitespace below text after adding many lines of text. The initial idea was to have a window of fixed height and this was achieved by switching ipady in the grid definition to height=9
