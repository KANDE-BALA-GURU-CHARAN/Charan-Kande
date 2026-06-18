"""Typing Speed Test mini project."""

import random
import time
import tkinter as tk


SENTENCES = [
    "Python makes programming simple and powerful.",
    "Practice improves typing speed and accuracy.",
    "A good program solves a real problem clearly.",
    "Keyboard events help programs respond to users.",
]


class TypingSpeedTest(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.geometry("720x430")
        self.configure(bg="#f8fafc")
        self.start_time = None
        self.target = ""

        tk.Label(self, text="Typing Speed Test", font=("Segoe UI", 20, "bold"), bg="#f8fafc").pack(pady=(22, 8))
        self.prompt = tk.Message(self, text="", width=650, font=("Segoe UI", 14), bg="#ffffff", relief="solid", bd=1, padx=12, pady=12)
        self.prompt.pack(pady=12)

        self.input_box = tk.Text(self, height=5, width=74, font=("Segoe UI", 12), state="disabled", wrap="word")
        self.input_box.pack(pady=8)
        self.input_box.bind("<KeyRelease>", self.update_results)

        buttons = tk.Frame(self, bg="#f8fafc")
        buttons.pack(pady=8)
        tk.Button(buttons, text="Start", width=10, command=self.start_test).grid(row=0, column=0, padx=6)
        tk.Button(buttons, text="Reset", width=10, command=self.reset_test).grid(row=0, column=1, padx=6)

        self.result = tk.Label(self, text="Click Start to begin.", bg="#f8fafc", font=("Segoe UI", 11))
        self.result.pack(pady=8)

    def start_test(self):
        self.target = random.choice(SENTENCES)
        self.prompt.config(text=self.target)
        self.input_box.config(state="normal")
        self.input_box.delete("1.0", "end")
        self.input_box.focus_set()
        self.start_time = time.time()
        self.result.config(text="Typing...")

    def reset_test(self):
        self.start_time = None
        self.target = ""
        self.prompt.config(text="")
        self.input_box.config(state="normal")
        self.input_box.delete("1.0", "end")
        self.input_box.config(state="disabled")
        self.result.config(text="Click Start to begin.")

    def update_results(self, _event=None):
        if self.start_time is None:
            return
        typed = self.input_box.get("1.0", "end-1c")
        elapsed = max(time.time() - self.start_time, 1)
        words = len(typed.split())
        wpm = words / (elapsed / 60)
        correct_chars = sum(1 for typed_char, target_char in zip(typed, self.target) if typed_char == target_char)
        accuracy = (correct_chars / max(len(self.target), 1)) * 100
        self.result.config(text=f"Time: {elapsed:.1f}s   WPM: {wpm:.1f}   Accuracy: {accuracy:.1f}%")
        if typed == self.target:
            self.input_box.config(state="disabled")
            self.result.config(text=f"Finished! Time: {elapsed:.1f}s   WPM: {wpm:.1f}   Accuracy: 100.0%")


if __name__ == "__main__":
    TypingSpeedTest().mainloop()
