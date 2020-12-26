This is a Python Coder Encoder miniproject by Jan Grottel. 
Started on 23.12.2020

Parameters:
Write an app that encodes a message and decodes it using a custom key.
With a basic tkinter GUI and base64 library code

Elements that will be needed as of project start:
1. A tkinter GUi to input message
2. A way to switch from code decode modes
3. A function that will encode decode a message given the message and the key.
4. A way to output the message in the GUI
5. Any additional features are deemed unnecessary feature bloat at this point.

Post-mortem:
1. Quick little exercise, mostly spent on the ui elements and error catching
2. Once again modular build, the function is independent of the GUI
3. The encoding itself is interesting, but adding of the key is unique. This was grabbed from the solution at the website as it was unclear to me how it should work.
4. The test functions went through a transformation when I grabbed errors - no key/no message is not an error as intended at the start but encodes correctly (without a key if no key).
5. I experimented with the custom class for a label - all labels use the same padding so may as well save some writing.

Unexpected things learned:
1. base64 is now named pybase64
2. Very interesting approach to avoiding negative values for ords when recording - add the range (256) as we care about the modulo values only!
3. A little confusion with tkinter variables - they have to be set() and get() as opposed to regular python vars
4. Decoding a message that's not in the correct format throws an error not native to pybase64 module. Had to import another module as a hotfix.