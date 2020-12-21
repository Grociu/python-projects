This is a python E-mail Address Grabber by Jan Grottel. Started on 17.12.2020

Parameters:
Write an app that grabs all e-mail addresses from a website, when given url.

Elements that will be needed as of project start:
1. A tkinter interface for the user to input and output
2. Input box for pasting an URL
3. Button for executing the script
    a) webscrapping via beautiful soup
    b) regex.findall should do the job
4. Message box for feedback (depending on the input/scrapping error)
5. Output box:
    a) scrapped e-mail addresses each on a new line
    b) the user has to be able to C&P the e-mail addresses from here!
6. Write to file button
7. Any additional features are deemed unnecessary feature bloat at this point.

Post-mortem:
1. I'm now much more happy with the modular nature of this app - the global functions could be reused as is by importing or copy and paste. This required a refactor after initial programming, but I'm very glad I did it.
2. Modular nature of the code allowed me to unittest the function to grab e-mails
independently of the GUI, which I think is not a bad practice.
3. I found a really comprehensive beautiful soup video tutorial:
https://www.youtube.com/watch?v=GjKQ6V_ViQE
It really opened my eyes to the potential (and ease of webscrapping)
4. e-mail validation is well research on the web, there are many e-mail addresses that are surprisingly valid. I used a basic
5. I created a custom Exception for my function as a catch all for requests validations errors. This could be tested more with different error codes if needed.

Unexpected things learned:
1. The current e-mail validation regex suggested on Stack Overflow is really 
long and I think beyond a regular human's ability to comprehend.
2. Putting a tk.Tk into a class of it's own is much more useful - avoids global
variable declarations which I think is better code
3. self.title = "Title" was not correct - tk.Tk.title is a function! so I changed it to self.title("Title")
4. Not sure if I completely understand the write to file functionality I found on the web,but I'm missing essential information about working with files, I need more work on the os, sys modules and files in general.
5. This program shows me how easy it is to get plaintext e-mail addresses from the web, I also noticed that most contact us pages don't actually include the verbatim address, it's always nested in an app or form of some sort.
6. tkinter went through a change of some sort recently cause arguments like 0, END don't really work, and need to have '0' and 'end'. might be P2 vs P3
7. tk.Text has absolutely unclear indexing '1.0' is start!
