"""Catch the Falling Objects mini project."""

import random
import tkinter as tk
from tkinter import messagebox


class CatchGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catch the Falling Objects")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")

        self.canvas = tk.Canvas(self, width=480, height=520, bg="#e0f2fe", highlightthickness=0)
        self.canvas.pack(padx=20, pady=(20, 8))
        self.status = tk.Label(self, text="", bg="#f8fafc", font=("Segoe UI", 12, "bold"))
        self.status.pack()
        tk.Button(self, text="New Game", command=self.new_game).pack(pady=8)

        self.bind("<Left>", lambda _event: self.move_basket(-30))
        self.bind("<Right>", lambda _event: self.move_basket(30))
        self.canvas.bind("<Motion>", self.follow_mouse)

        self.objects = []
        self.running = False
        self.timer_id = None
        self.new_game()

    def new_game(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.canvas.delete("all")
        self.score = 0
        self.lives = 3
        self.objects = []
        self.running = True
        self.basket = self.canvas.create_rectangle(200, 485, 280, 510, fill="#2563eb", outline="")
        self.update_status()
        self.animate()

    def update_status(self):
        self.status.config(text=f"Score: {self.score}   Lives: {self.lives}")

    def move_basket(self, dx):
        x1, y1, x2, y2 = self.canvas.coords(self.basket)
        if x1 + dx < 0:
            dx = -x1
        if x2 + dx > 480:
            dx = 480 - x2
        self.canvas.move(self.basket, dx, 0)

    def follow_mouse(self, event):
        x1, _y1, x2, _y2 = self.canvas.coords(self.basket)
        center = (x1 + x2) / 2
        self.move_basket(event.x - center)

    def spawn_object(self):
        x = random.randint(15, 465)
        size = random.randint(16, 24)
        item = self.canvas.create_oval(x - size, 0, x + size, size * 2, fill="#f97316", outline="")
        speed = random.randint(4, 8)
        self.objects.append((item, speed))

    def animate(self):
        if not self.running:
            return
        if random.random() < 0.08:
            self.spawn_object()

        basket_coords = self.canvas.coords(self.basket)
        remaining = []
        for item, speed in self.objects:
            self.canvas.move(item, 0, speed)
            coords = self.canvas.coords(item)
            if self.collides(coords, basket_coords):
                self.canvas.delete(item)
                self.score += 1
            elif coords[1] > 520:
                self.canvas.delete(item)
                self.lives -= 1
            else:
                remaining.append((item, speed))
        self.objects = remaining
        self.update_status()

        if self.lives <= 0:
            self.running = False
            messagebox.showinfo("Game Over", f"Final score: {self.score}")
            return
        self.timer_id = self.after(35, self.animate)

    def collides(self, a, b):
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


if __name__ == "__main__":
    CatchGame().mainloop()
