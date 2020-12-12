This is a Python Rock, Paper, Scissors game project by Jan Grottel, started 24.11.2020.

Parameters:
Write a rock, paper, scissors game for one or two players. Implement a basic UI.

Elements that will be needed as of project start:
1. A basic 'type' system for possible choices and outcomes:
    a) a 'type' for rock paper scissors, includes only these options
    b) a 'type' for player_1_win, draw, player_2_win, includes only these options
While not strictly needed to implement the game aspect of the project, I know this is a possible thing to create so I want to refresh.
2. Function rock_paper_scissors on the types from point 1, unit tested.
3. A select screen for number of players (1 or 2)
4. A basic 'AI' bot that will select a random choice.
5. Object that's the main screen with two subclasses (?)
6. A main game screen for 1 player game, divided in two.
    a) buttons to choose your pick, on the left, instructions
    b) your choices are confirmed, message
    c) outcome screen with try again button
    d) running tally of results (unittested?)
6. A main game screen for 2 player game, divided in two
    a) instead of buttons, keyboard shortcuts for left/right side of keyboard. with instructions
    b) detect keystrokes
    c) your outcomes are confirmed
    d) outcome screen, try again button
    e) running tally of results
7. Probably a quit button somewhere.
8. Testing module - test the functions of the game if possible.
9. Any additional features are deemed unnecessary feature bloat at this point.

Things to learn:
1. Custom datatypes.
2. Basic UI - tkinter module. I have no idea how that works.
3. Design of classes for windows - inheritance of the main class.
4. Detecting keystrokes, waiting for outcomes.

And as always:
5. Designing the program first using functions, classes and pass statements.
6. Building the test functions second.
7. Coding third.
8. Commenting on code while coding.

Post-mortem:
1. Going through a comprehensive tkinter tutorial took a lot of time.
2. While main logic of the game took just a few minutes to implement, the GUI elements took ages to get just right.
3. It was a good exercise to create custom classes as subclasses of tk.LabelFrame - I learned a bit about class inheritance and the super() function.
The class idea was the best one I had during this project.
4. Keyboard shortcuts feel hacky at best. They work though.
5. Not sure about the updating of widgets with input. Clicking a button grid_forgets() a widget, edits it and places it back. Maybe a dedicated function would do better?
6. Unittesting is tricky for these. A google search for tkinter unittesting reveals that it's definitely possible, but would require hours of research.
Another aspect of this is the idea of writing tests beforehand. As design of the app changed over time so would the tkinter tests - hard to maintain really
ex, let's say I want to unittest the output of 'games so far' labels. I have three labels each with different output (int) converted into string, all dependant on a list of games that happened. However originally this was one label that was changing its text dependant on something that I have not yet imagined. The tests would need to change to reflect new design.
Is that how I want to do things?
7. Custom data types (enumerations) were not really needed.
8. This project took way too long, for what it is.
9. I'm not happy with the file imports (images) here - there is very little universality. as my git directory is the python-projects dir. It just didn't feel natural to use the subdir in the code.

Unexpected things learned:
1. Inheritance isn't that easy of an concept as I originally thought, full research on OOP in Python is warranted especially full understanding of super()
2. Writing nice looking apps is hard and a real fuss. The 'meat' of the code was the rps function, the rest was just dressing! Yet the dressing took the longest.
3. Python is amazingly versatile. When stuck finding the answer was relatively easy, with multiple articles and StackOverflow questions. I don't expect c++ to have these.
4. I need a better understanding of the os module. It was not used here, but I think I need to do several scripts to fully utilize that library to see what's possible.
5. I didn't know of tkinter before this exercise, but it's really intuitive to use and a simple way to make the apps real (I'm sorry, command line python <3 )
6. A subclass does not automatically inherit it's parents __init___ methods on args and kwargs!
7. Basic tkinter popup boxes are quite limited.