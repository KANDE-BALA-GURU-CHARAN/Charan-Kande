"""Word Scramble Game mini project."""

import random
import tkinter as tk
from tkinter import messagebox


WORDS = [
    "python",
    "variable",
    "function",
    "loop",
    "condition",
    "string",
    "button",
    "canvas",
    "keyboard",
    "project",
]


class WordScramble(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Scramble Game")
        self.geometry("480x340")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")
        self.score = 0
        self.round_no = 0
        self.answer = ""

        tk.Label(self, text="Word Scramble Game", font=("Segoe UI", 20, "bold"), bg="#f8fafc").pack(pady=(24, 8))
        self.scrambled_label = tk.Label(self, text="", font=("Consolas", 28, "bold"), bg="#f8fafc", fg="#1d4ed8")
        self.scrambled_label.pack(pady=18)

        self.guess_entry = tk.Entry(self, width=24, font=("Segoe UI", 14), justify="center")
        self.guess_entry.pack(pady=6)
        self.guess_entry.bind("<Return>", lambda _event: self.check_answer())

        buttons = tk.Frame(self, bg="#f8fafc")
        buttons.pack(pady=12)
        tk.Button(buttons, text="Check", width=10, command=self.check_answer).grid(row=0, column=0, padx=6)
        tk.Button(buttons, text="Skip", width=10, command=self.next_word).grid(row=0, column=1, padx=6)

        self.status = tk.Label(self, text="", bg="#f8fafc", font=("Segoe UI", 11))
        self.status.pack(pady=6)
        self.next_word()

    def scramble(self, word):
        letters = list(word)
        for _ in range(20):
            random.shuffle(letters)
            scrambled = "".join(letters)
            if scrambled != word:
                return scrambled
        return word[::-1]

    def next_word(self):
        self.answer = random.choice(WORDS)
        self.round_no += 1
        self.guess_entry.delete(0, "end")
        self.scrambled_label.config(text=self.scramble(self.answer))
        self.update_status()

    def check_answer(self):
        guess = self.guess_entry.get().strip().lower()
        if guess == self.answer:
            self.score += 1
            messagebox.showinfo("Correct", "Great job!")
            self.next_word()
        else:
            messagebox.showwarning("Try Again", "That is not the correct word.")

    def update_status(self):
        self.status.config(text=f"Round: {self.round_no}   Score: {self.score}")


if __name__ == "__main__":
    WordScramble().mainloop()
