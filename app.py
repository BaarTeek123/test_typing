import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

from Config import Config
from RealTimeListener import RealTimeKeyListener
from sentence_generator import generate_sentence


class TypingTestGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Test")

        self.target_sentence = random.choice(generate_sentence(Config.SENTENCES_FILE))
        self.key_listener = RealTimeKeyListener()

        self.label = tk.Label(master, text="Type this sentence:")
        self.label.pack()

        self.target_text = tk.Text(master, height=2, width=50)
        self.target_text.pack()
        self.target_text.insert(tk.END, self.target_sentence)
        self.target_text.config(state=tk.DISABLED)

        self.input_text = tk.Text(master, height=2, width=50)
        self.input_text.pack()
        self.input_text.bind("<Key>", self.key_listener.get_sentence())
        self.input_text.focus_set()

        self.start_time = time.time()

        self.status_label = tk.Label(master, text="Start typing")
        self.status_label.pack()

    def on_key_press(self, event=None):
        typed_sentence = self.input_text.get("1.0", tk.END).strip()
        if typed_sentence == self.target_sentence:
            elapsed_time = time.time() - self.start_time
            messagebox.showinfo("Completed", f"Well done! You've completed the test in {elapsed_time:.2f} seconds.")
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestGUI(root)
    root.mainloop()