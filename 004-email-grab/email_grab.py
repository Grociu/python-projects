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
    Grabs wordlike strings that look like e-mail addresses from a long string
    Returns a list of strings (e-mails)
    Using a basic regex pattern, nothing too fancy
    """
    email_match = re.compile(
        r"""
        \b                # at the start of a word
        [a-zA-Z0-9_.+-]+  # match a sequence of at least 1 ch num _ . + or -
        @                 # then a single @
        [a-zA-Z0-9-]+     # domain names similar to username
        \.                # a literal dot
        [a-zA-Z0-9-.]+    # then more letters/numbers
        \b                # at the end of a word
        """, re.X         # same as re.VERBOSE, enable use of comments here
        )
    return re.findall(email_match, text)


def execute():
    global feedback
    global output_window
    """ Function that runs when the get Run button is pushed """
    output_window.delete('1.0', 'end')
    url = input_window.get()
    try:
        soup = cook_soup(url)
        text = soup.get_text()
        emails = grab_emails(text)
        output_window.insert('end', ", \n".join(emails))
        feedback['fg'] = 'green'
        feedback['text'] = 'Executed correctly'
    except requests.exceptions.MissingSchema:
        feedback['fg'] = 'red'
        feedback['text'] = 'Request error, Invalid URL\nTry adding http://'


root = tk.Tk()
root.title("E-mail Address Grabber")
root.geometry("600x300")

input_window_label = tk.Label(root, text="Paste URL here:")
input_window_label.grid(row=0, column=0, padx=5)

input_window = tk.Entry(root, width=70)
input_window.grid(row=0, column=1, padx=5)

submit_button = tk.Button(root, text="Run", command=execute)
submit_button.grid(row=0, column=2, padx=5, ipadx=4)

feedback_label = tk.Label(root, text="Progress:")
feedback_label.grid(row=4, column=0)

feedback = tk.Label(root, text="", fg="red")
feedback.grid(row=5, column=1, columnspan=2)

output_label = tk.Label(root, text="Output:")
output_label.grid(row=6, column=0)

output_window = tk.Text(root, height=12, width=65)
output_window.grid(row=7, column=0, columnspan=3, padx=10)


if __name__ == '__main__':
    root.mainloop()
