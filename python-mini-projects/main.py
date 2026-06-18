"""Launcher for the Python mini project collection."""

from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


ROOT = Path(__file__).resolve().parent

PROJECTS = [
    ("Alarm Clock", "projects/01_alarm_clock/alarm_clock.py"),
    ("Drawing Pad", "projects/02_drawing_pad/drawing_pad.py"),
    ("To-Do List and Reminders", "projects/03_todo_reminders/todo_reminders.py"),
    ("Attendance Management System", "projects/04_attendance_management/attendance_management.py"),
    ("Expense Tracker", "projects/05_expense_tracker/expense_tracker.py"),
    ("Weather App", "projects/06_weather_app/weather_app.py"),
    ("Memory Card Matching Game", "projects/07_memory_card_game/memory_card_game.py"),
    ("Word Scramble Game", "projects/08_word_scramble/word_scramble.py"),
    ("Typing Speed Test", "projects/09_typing_speed_test/typing_speed_test.py"),
    ("Catch the Falling Objects", "projects/10_catch_falling_objects/catch_falling_objects.py"),
    ("Animal Identification Game", "projects/11_animal_identification/animal_identification.py"),
    ("Puzzle Rearrangement Game", "projects/12_puzzle_rearrangement/puzzle_rearrangement.py"),
]


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Mini Projects")
        self.geometry("520x560")
        self.resizable(False, False)
        self.configure(bg="#f6f7fb")

        tk.Label(
            self,
            text="Python Mini Projects",
            font=("Segoe UI", 20, "bold"),
            bg="#f6f7fb",
            fg="#1f2937",
        ).pack(pady=(20, 4))
        tk.Label(
            self,
            text="Select a project to open",
            font=("Segoe UI", 11),
            bg="#f6f7fb",
            fg="#4b5563",
        ).pack(pady=(0, 14))

        frame = tk.Frame(self, bg="#f6f7fb")
        frame.pack(fill="both", expand=True, padx=28, pady=8)

        for name, path in PROJECTS:
            button = tk.Button(
                frame,
                text=name,
                anchor="w",
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#111827",
                relief="solid",
                bd=1,
                padx=12,
                pady=7,
                command=lambda project_path=path: self.launch(project_path),
            )
            button.pack(fill="x", pady=4)

    def launch(self, project_path):
        script = ROOT / project_path
        if not script.exists():
            messagebox.showerror("Missing File", f"Could not find:\n{script}")
            return
        subprocess.Popen([sys.executable, str(script)], cwd=str(script.parent))


if __name__ == "__main__":
    Launcher().mainloop()
