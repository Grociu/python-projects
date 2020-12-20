from bs4 import BeautifulSoup as bs
import re
import requests
import tkinter as tk


def cook_soup(link):
    """ Creates a BeautifulSoup object from an url """
    request = requests.get(link)
    soup = bs(request.content)
    return soup


def grab_emails(text):
    """
    Grabs strings that look like e-mail addresses from a long string
    Returns a list of strings (e-mails)
    Using a basic regex pattern, nothing too fancy
    """
    email_match = re.compile(
        r"""
        ^                 # at the start of the string
        [a-zA-Z0-9_.+-]+  # match a sequence of at least 1 ch num _ . + or -
        @                 # then a single @
        [a-zA-Z0-9-]+     # domain names similar to username
        \.                # a literal dot
        [a-zA-Z0-9-.]+    # then more letters/numbers
        $                 # at the end of the string
        """, re.X         # same as re.VERBOSE, enable use of comments here
        )
    return re.findall(email_match, text)


root = tk.Tk()
root.title("E-mail Address Grabber")
root.geometry("600x200")

input_window_label = tk.Label(root, text="Paste URL here:")
input_window_label.grid(row=0, column=0, padx=5)

input_window = tk.Entry(root, width=70)
input_window.grid(row=0, column=1, padx=5)

# submit_button_label = tk.Label(root, text="Run Script to get e-mail addresses")
# submit_button_label.grid(row=2, column=0)

submit_button = tk.Button(root, text="Run")
submit_button.grid(row=0, column=2, padx=5, ipadx=4)

feedback_label = tk.Label(root, text="Progress:")
feedback_label.grid(row=4, column=0)

feedback = tk.Label(root, text="")
feedback.grid(row=5, column=0)

output_label = tk.Label(root, text="Output:")
output_label.grid(row=6, column=0)

output_window = tk.Label(root, text="")
output_window.grid(row=7, column=0)


if __name__ == '__main__':
    root.mainloop()
