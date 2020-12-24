import pybase64
import tkinter as tk


def encode_message(key, message):
    """ Encodes the message (string) using the key (string) and
    pybase64.urlsafe_b64encode functionality """

    keycoded = []

    if not key:
        key = chr(0)

    # iterating through the message
    for i in range(len(message)):
        # assigning a key_character based on the given key
        key_character = key[i % len(key)]
        # each char of the message has the key_char added (in ascii values)
        # and is converted back to normal, and appended to the keycoded values
        keycoded.append(
            chr((ord(message[i]) + ord(key_character)) % 256)
        )

    encoded = pybase64.urlsafe_b64encode(
        "".join(keycoded).encode()  # convert to bytes object (builtin)
        ).decode()  # back to text

    return encoded


def decode_message(key, message):
    """ Decodes the message (string) using the key (string) and
    pybase64.urlsafe_b64encode functionality """

    message_bytes = message.encode()  # convert to a bytes object

    decoded_but_keyed = pybase64.urlsafe_b64decode(message_bytes).decode()

    # retreive original message using the key
    dekeyed = []

    if not key:
        key = chr(0)

    # iterating through the message
    for i in range(len(decoded_but_keyed)):
        # assigning a key_character based on the given key
        key_character = key[i % len(key)]
        # each char of the message has the key_char substracted (in ascii vals)
        # and is converted back to normal, and appended to the dekeyed values
        dekeyed.append(
            chr((256 + ord(decoded_but_keyed[i]) - ord(key_character)) % 256)
        )

    decoded = "".join(dekeyed)
    return decoded


# Class for this app's labels
class EncoderLabel(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self['padx'] = 10
        self['pady'] = 5


# Class for the main GUI element
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("425x410")
        self.title("Encoder/Decoder")
        # self.resizable(0,0)
        # Setup variable for the program mode
        self.mode = tk.StringVar()
        self.mode.set('Encode')
        # Place the GUI elements inside the app
        self.place_elements()

    def place_elements(self):
        # Header for the common key
        self.key_label = EncoderLabel(self, text="Enter the common key:")
        self.key_label.grid(row=0, column=0, columnspan=2, sticky='w')

        # Input field for common key entry
        self.input_key_field = tk.Entry(self, width=40)
        self.input_key_field.grid(
            row=1, column=0, columnspan=2, padx=5, sticky='w'
        )

        # Header for the message to encode
        self.message_label = EncoderLabel(self, text="Enter the message:")
        self.message_label.grid(row=2, column=0, columnspan=2, sticky='w')

        # Input field for entering the message/code
        self.message_input_field = tk.Entry(self, width=40)
        self.message_input_field.grid(
            row=3, column=0, columnspan=2, sticky='ew', padx=5
        )

        # Header for selecting mode Encode/Decode
        self.select_mode_label = EncoderLabel(self, text="Select mode:")
        self.select_mode_label.grid(
            row=4, column=0, columnspan=2, sticky='w'
        )

        # Selector for mode (radio buttons)
        self.encode_mode_button = tk.Radiobutton(
            self, text="Encode mode", variable=self.mode, value="Encode"
        )
        self.encode_mode_button.grid(row=5, column=0)

        self.decode_mode_button = tk.Radiobutton(
            self, text="Decode mode", variable=self.mode, value="Decode"
        )
        self.decode_mode_button.grid(row=5, column=1)

        # Execute button
        self.execute_button = tk.Button(
            self, text="Execute", command=self.execute,
        )
        self.execute_button.grid(row=6, column=0, ipadx=10, columnspan=2)

        # Header for the encoded/decoded message
        self.encoded_label = EncoderLabel(self, text="Encoded/Decode message:")
        self.encoded_label.grid(row=7, column=0, columnspan=2, sticky='w')

        # Text field with the encoded/decoded message
        self.output_window = tk.Text(self, height=10, width=50)
        self.output_window.grid(
            row=8, column=0, columnspan=2, sticky='w', padx=5, pady=10
        )

    def execute(self):
        """
        Executes the encoding/decoding process with a given message and key.
        """
        # Grab the key:
        key = self.input_key_field.get()

        # Grab the message:
        message = self.message_input_field.get()

        # Clear the output field:
        self.output_window.delete('1.0', 'end')

        # Update the output field
        if self.mode.get() == 'Encode':
            self.output_window.insert('end', encode_message(key, message))
        elif self.mode.get() == 'Decode':
            self.output_window.insert('end', decode_message(key, message))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
