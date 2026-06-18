"""Puzzle Rearrangement Game mini project."""

import random
import tkinter as tk
from tkinter import messagebox


class SlidingPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Puzzle Rearrangement Game")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")
        self.moves = 0

        tk.Label(self, text="Puzzle Rearrangement Game", font=("Segoe UI", 17, "bold"), bg="#f8fafc").pack(pady=(20, 8))
        self.status = tk.Label(self, text="", bg="#f8fafc", font=("Segoe UI", 11))
        self.status.pack()

        board = tk.Frame(self, bg="#f8fafc")
        board.pack(pady=20)
        self.buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = tk.Button(
                    board,
                    width=6,
                    height=3,
                    font=("Segoe UI", 18, "bold"),
                    command=lambda r=row, c=col: self.move_tile(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        tk.Button(self, text="Shuffle", width=12, command=self.shuffle_board).pack(pady=6)
        self.board = []
        self.shuffle_board()

    def shuffle_board(self):
        self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        blank = (2, 2)
        for _ in range(120):
            neighbors = self.neighbors(*blank)
            row, col = random.choice(neighbors)
            self.board[blank[0]][blank[1]], self.board[row][col] = self.board[row][col], self.board[blank[0]][blank[1]]
            blank = (row, col)
        self.moves = 0
        self.refresh()

    def neighbors(self, row, col):
        result = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                result.append((nr, nc))
        return result

    def find_blank(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return row, col
        return 2, 2

    def move_tile(self, row, col):
        blank = self.find_blank()
        if (row, col) not in self.neighbors(*blank):
            return
        br, bc = blank
        self.board[br][bc], self.board[row][col] = self.board[row][col], self.board[br][bc]
        self.moves += 1
        self.refresh()
        if self.is_solved():
            messagebox.showinfo("Solved", f"Puzzle solved in {self.moves} moves!")

    def refresh(self):
        for row in range(3):
            for col in range(3):
                value = self.board[row][col]
                if value == 0:
                    self.buttons[row][col].config(text="", bg="#e5e7eb", state="disabled")
                else:
                    self.buttons[row][col].config(text=str(value), bg="#bfdbfe", state="normal")
        self.status.config(text=f"Moves: {self.moves}")

    def is_solved(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


if __name__ == "__main__":
    SlidingPuzzle().mainloop()
