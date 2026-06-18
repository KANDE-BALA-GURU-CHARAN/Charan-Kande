"""To-Do List and Reminders mini project."""

import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


DATA_FILE = Path(__file__).with_name("tasks.json")


class TodoReminders(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List and Reminders")
        self.geometry("620x430")
        self.configure(bg="#f8fafc")
        self.tasks = []

        top = tk.Frame(self, bg="#f8fafc", padx=12, pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Task", bg="#f8fafc").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(top, width=36)
        self.task_entry.grid(row=1, column=0, padx=(0, 8), sticky="w")

        tk.Label(top, text="Reminder HH:MM", bg="#f8fafc").grid(row=0, column=1, sticky="w")
        self.reminder_entry = tk.Entry(top, width=14)
        self.reminder_entry.grid(row=1, column=1, sticky="w")

        tk.Button(top, text="Add Task", command=self.add_task).grid(row=1, column=2, padx=8)

        body = tk.Frame(self, bg="#f8fafc", padx=12)
        body.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(body, height=14, font=("Segoe UI", 10))
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(body, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        actions = tk.Frame(body, bg="#f8fafc")
        actions.pack(side="left", fill="y", padx=10)
        tk.Button(actions, text="Delete", width=12, command=self.delete_task).pack(pady=4)
        tk.Button(actions, text="Clear All", width=12, command=self.clear_tasks).pack(pady=4)

        self.status = tk.Label(self, text="", bg="#f8fafc", fg="#475569")
        self.status.pack(fill="x", padx=12, pady=8)

        self.load_tasks()
        self.refresh_list()
        self.check_reminders()

    def load_tasks(self):
        if DATA_FILE.exists():
            try:
                self.tasks = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.tasks = []

    def save_tasks(self):
        DATA_FILE.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")

    def add_task(self):
        text = self.task_entry.get().strip()
        reminder = self.reminder_entry.get().strip()
        if not text:
            messagebox.showwarning("Missing Task", "Please enter a task.")
            return
        if reminder and not self.valid_time(reminder):
            messagebox.showerror("Invalid Reminder", "Reminder must be in HH:MM format.")
            return
        self.tasks.append({"text": text, "reminder": reminder, "reminded": False})
        self.task_entry.delete(0, "end")
        self.reminder_entry.delete(0, "end")
        self.save_tasks()
        self.refresh_list()

    def valid_time(self, value):
        parts = value.split(":")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            return False
        hour, minute = map(int, parts)
        return 0 <= hour <= 23 and 0 <= minute <= 59

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        del self.tasks[selection[0]]
        self.save_tasks()
        self.refresh_list()

    def clear_tasks(self):
        if messagebox.askyesno("Clear Tasks", "Delete all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, "end")
        for task in self.tasks:
            reminder = f" at {task['reminder']}" if task.get("reminder") else ""
            self.listbox.insert("end", f"{task['text']}{reminder}")
        self.status.config(text=f"Total tasks: {len(self.tasks)}")

    def check_reminders(self):
        import datetime as dt

        now = dt.datetime.now().strftime("%H:%M")
        changed = False
        for task in self.tasks:
            if task.get("reminder") == now and not task.get("reminded"):
                task["reminded"] = True
                changed = True
                self.bell()
                messagebox.showinfo("Reminder", task["text"])
        if changed:
            self.save_tasks()
            self.refresh_list()
        self.after(30000, self.check_reminders)


if __name__ == "__main__":
    TodoReminders().mainloop()
