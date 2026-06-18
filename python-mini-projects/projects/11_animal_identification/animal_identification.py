"""Animal Identification Game mini project."""

import random
import tkinter as tk
from tkinter import messagebox


ANIMALS = ["Cat", "Dog", "Rabbit", "Fish"]


class AnimalGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Animal Identification Game")
        self.geometry("520x470")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")
        self.score = 0
        self.question = 0
        self.answer = ""
        self.image = None

        tk.Label(self, text="Animal Identification Game", font=("Segoe UI", 18, "bold"), bg="#f8fafc").pack(pady=(18, 6))
        self.image_label = tk.Label(self, bg="#ffffff", relief="solid", bd=1)
        self.image_label.pack(pady=12)

        self.buttons_frame = tk.Frame(self, bg="#f8fafc")
        self.buttons_frame.pack(pady=8)
        self.option_buttons = []
        for index in range(4):
            button = tk.Button(self.buttons_frame, width=14, command=lambda i=index: self.check_answer(i))
            button.grid(row=index // 2, column=index % 2, padx=8, pady=6)
            self.option_buttons.append(button)

        self.status = tk.Label(self, text="", bg="#f8fafc", font=("Segoe UI", 11))
        self.status.pack(pady=8)
        tk.Button(self, text="Next", command=self.next_question).pack()
        self.next_question()

    def make_image(self, animal):
        image = tk.PhotoImage(width=220, height=160)
        image.put("#e0f2fe", to=(0, 0, 220, 160))

        def rect(color, x1, y1, x2, y2):
            image.put(color, to=(x1, y1, x2, y2))

        if animal == "Cat":
            rect("#f59e0b", 70, 50, 150, 125)
            rect("#f59e0b", 58, 34, 82, 58)
            rect("#f59e0b", 138, 34, 162, 58)
            rect("#111827", 88, 78, 98, 88)
            rect("#111827", 122, 78, 132, 88)
            rect("#ffffff", 106, 94, 116, 104)
            rect("#111827", 52, 98, 84, 102)
            rect("#111827", 136, 98, 168, 102)
        elif animal == "Dog":
            rect("#92400e", 75, 48, 145, 122)
            rect("#78350f", 50, 58, 76, 116)
            rect("#78350f", 144, 58, 170, 116)
            rect("#111827", 91, 76, 101, 86)
            rect("#111827", 119, 76, 129, 86)
            rect("#facc15", 94, 96, 126, 116)
            rect("#111827", 106, 100, 116, 108)
        elif animal == "Rabbit":
            rect("#f3f4f6", 78, 62, 142, 132)
            rect("#f3f4f6", 82, 20, 102, 72)
            rect("#f3f4f6", 118, 20, 138, 72)
            rect("#f9a8d4", 88, 30, 96, 66)
            rect("#f9a8d4", 124, 30, 132, 66)
            rect("#111827", 94, 88, 104, 98)
            rect("#111827", 116, 88, 126, 98)
        else:
            rect("#22c55e", 50, 72, 145, 112)
            rect("#16a34a", 145, 82, 180, 102)
            rect("#bbf7d0", 30, 82, 55, 102)
            rect("#111827", 70, 84, 80, 94)
            rect("#86efac", 95, 62, 116, 78)

        return image

    def next_question(self):
        self.answer = random.choice(ANIMALS)
        self.question += 1
        self.image = self.make_image(self.answer)
        self.image_label.config(image=self.image)
        options = ANIMALS[:]
        random.shuffle(options)
        self.current_options = options
        for button, option in zip(self.option_buttons, options):
            button.config(text=option)
        self.update_status()

    def check_answer(self, index):
        choice = self.current_options[index]
        if choice == self.answer:
            self.score += 1
            messagebox.showinfo("Correct", "Correct answer!")
            self.next_question()
        else:
            messagebox.showwarning("Incorrect", f"Wrong answer. It was {self.answer}.")
            self.next_question()

    def update_status(self):
        self.status.config(text=f"Question: {self.question}   Score: {self.score}")


if __name__ == "__main__":
    AnimalGame().mainloop()
