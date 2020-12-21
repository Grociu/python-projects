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
        self.title = "E-mail Address Grabber"
        self.geometry = "600x300"
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


if __name__ == '__main__':
    App = MainApplication()
    App.mainloop()
