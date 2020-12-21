from bs4 import BeautifulSoup as bs
import re
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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


class InvalidURLError(Exception):
    """Exception raised if the URL input is invalid
    Attributes:
        expression -- input that caused the error
        message -- explanation of the error
    """
    def __init__(self, expression, message="Invalid URL, try adding http://"):
        self.expression = expression
        self.message = message


def get_all_email_addresses(link):
    """
    Provided an url as string, returns a list of all valid e-mail addresses
    In the target website.
    Raises an InvalidURLError exception if a request is bad
    """
    try:
        soup = cook_soup(link)
        text = soup.get_text()
        emails = grab_emails(text)
        return emails
    except requests.exceptions.MissingSchema:
        raise InvalidURLError(link)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-mail Address Grabber")
        self.geometry("600x350")
        self.elements_startup()

    def elements_startup(self):
        """ Initializes widgets of the app """
        self.input_window_label = tk.Label(self, text="Paste URL here:")
        self.input_window_label.grid(row=0, column=0, padx=5)

        self.input_window = tk.Entry(self, width=70)
        self.input_window.insert(  # Added as an example of functionality
            0, "https://en.wikipedia.org/wiki/Email_address"
            )
        self.input_window.grid(row=0, column=1, padx=5)

        self.submit_button = tk.Button(
            self, text="Run", command=self.execute
            )
        self.submit_button.grid(row=0, column=2, padx=5, ipadx=4)

        self.feedback_label = tk.Label(self, text="Progress:")
        self.feedback_label.grid(row=4, column=0)

        self.feedback = tk.Label(self, text="", fg="red")
        self.feedback.grid(row=5, column=1, columnspan=2)

        self.output_label = tk.Label(self, text="Output:")
        self.output_label.grid(row=6, column=0)

        self.output_window = tk.Text(self, height=12, width=65)
        self.output_window.grid(row=7, column=0, columnspan=3, padx=10)

        self.write_to_file_button = tk.Button(
            self, text="Save to file", command=self.save)
        self.write_to_file_button.grid(row=8, column=1, pady=5, sticky='e')

    def execute(self):
        """ Function that runs when the get Run button is pushed """
        self.output_window.delete('1.0', 'end')
        url = self.input_window.get()
        try:
            emails = get_all_email_addresses(url)
            self.output_window.insert('end', ", \n".join(emails))
            self.feedback['fg'] = 'green'
            self.feedback['text'] = 'Executed correctly'
        except InvalidURLError:
            self.feedback['fg'] = 'red'
            self.feedback['text'] = (
                'Request error, Invalid URL\nTry adding http://'
            )

    def save(self):
        """ Saves the output of the output_window to a text file """
        save_text_as = filedialog.asksaveasfile(
            mode='w', defaultextension='.txt'
            )                             # asks the user to specify a filename

        if save_text_as:  # if a filename is selected
            text_to_save = self.output_window.get('1.0', 'end')  # get text
            save_text_as.write(text_to_save)  # write text to file
            save_text_as.close()  # close the file
        else:  # if user cancelled then:
            messagebox.showinfo("Error", "Cancelled")  # show a popup


if __name__ == '__main__':
    App = MainApplication()
    App.mainloop()
