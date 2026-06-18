"""Memory Card Matching Game mini project."""

import random
import tkinter as tk
from tkinter import messagebox


class MemoryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Card Matching Game")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")
        self.buttons = []
        self.first = None
        self.second = None
        self.moves = 0
        self.matches = 0

        tk.Label(self, text="Memory Card Matching Game", font=("Segoe UI", 16, "bold"), bg="#f8fafc").pack(pady=14)
        self.status = tk.Label(self, text="", bg="#f8fafc", font=("Segoe UI", 11))
        self.status.pack()

        board = tk.Frame(self, bg="#f8fafc")
        board.pack(pady=16)
        for row in range(4):
            row_buttons = []
            for col in range(4):
                button = tk.Button(
                    board,
                    text="?",
                    width=6,
                    height=3,
                    font=("Segoe UI", 16, "bold"),
                    command=lambda r=row, c=col: self.flip_card(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        tk.Button(self, text="New Game", command=self.new_game).pack(pady=8)
        self.new_game()

    def new_game(self):
        values = list("AABBCCDDEEFFGGHH")
        random.shuffle(values)
        self.cards = [values[index : index + 4] for index in range(0, 16, 4)]
        self.revealed = [[False] * 4 for _ in range(4)]
        self.first = None
        self.second = None
        self.moves = 0
        self.matches = 0
        for row in range(4):
            for col in range(4):
                self.buttons[row][col].config(text="?", state="normal", bg="#e0f2fe")
        self.update_status()

    def flip_card(self, row, col):
        if self.revealed[row][col] or self.second is not None:
            return
        self.buttons[row][col].config(text=self.cards[row][col], bg="#ffffff")
        self.revealed[row][col] = True

        if self.first is None:
            self.first = (row, col)
            return

        self.second = (row, col)
        self.moves += 1
        self.update_status()
        self.after(700, self.check_match)

    def check_match(self):
        r1, c1 = self.first
        r2, c2 = self.second
        if self.cards[r1][c1] == self.cards[r2][c2]:
            self.matches += 1
            self.buttons[r1][c1].config(state="disabled", bg="#bbf7d0")
            self.buttons[r2][c2].config(state="disabled", bg="#bbf7d0")
        else:
            for row, col in (self.first, self.second):
                self.revealed[row][col] = False
                self.buttons[row][col].config(text="?", bg="#e0f2fe")
        self.first = None
        self.second = None
        self.update_status()
        if self.matches == 8:
            messagebox.showinfo("Winner", f"You matched all pairs in {self.moves} moves!")

    def update_status(self):
        self.status.config(text=f"Moves: {self.moves}   Matches: {self.matches}/8")


if __name__ == "__main__":
    MemoryGame().mainloop()
