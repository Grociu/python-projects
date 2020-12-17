import bs4
import requests
import tkinter as tk

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


root.mainloop()
