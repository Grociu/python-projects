This is a Python Target Practice game project by Jan Grottel. 
Started on 26.12.2020

Parameters:
Write an app that will contain a simple mouse target practice game.
Use the pygame module if possible.

I needed an interesting project to learn some pygame functionalities. 
The project will be preceeded by a pygame course with a sandbox-tutorial (not in this repository)
While most tutorials make snake or space invaders kind of games this is a little different.

Elements that will be needed as of project start:
1. The game screen:
    a) The meat of the game is this, a square on a blank screen in which you have to click with the mouse cursor.
    b) When you click on the square, it disappears and a smaller (somewhat) square appears elsewhere on the screen.
        > This will most likely be broken up to sections (splits) of 3-6 same size squares before getting smaller, but this will be done later in design process
    c) The task is to click all the progressively smaller squares as fast as possible.
    d) the user will be timed, with a timer akin to speedrunning timers - colorcoded! split times!, PB and so on!
    e) player represented by a crosshair of some sort
    f) results stored in a persisting database(?)
    g) a reset (new game button)
    h) a quit to main button
    i) quit button(?)
    j) instructions(?) - maybe on a splash screen before the game starts
    k) countdown(?)

2. Main menu:
    a) Start game button
    b) Quit button
    c) Best results button and screen (high scores):
        PB by split, best by split, potential best time
    d) Reset scores button (will be needed for debugging anyway)

3. Reserved for further feature descriptions