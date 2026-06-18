"""Expense Tracker mini project."""

import datetime as dt
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


DATA_FILE = Path(__file__).with_name("expenses.json")


class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("760x500")
        self.configure(bg="#f8fafc")
        self.expenses = []

        form = tk.Frame(self, bg="#f8fafc", padx=12, pady=12)
        form.pack(fill="x")
        self.date_entry = self.add_field(form, "Date", dt.date.today().isoformat(), 0)
        self.category_entry = self.add_field(form, "Category", "Food", 1)
        self.amount_entry = self.add_field(form, "Amount", "", 2)
        self.note_entry = self.add_field(form, "Note", "", 3)
        tk.Button(form, text="Add Expense", command=self.add_expense).grid(row=1, column=4, padx=8)

        columns = ("date", "category", "amount", "note")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for column, label, width in (
            ("date", "Date", 110),
            ("category", "Category", 140),
            ("amount", "Amount", 100),
            ("note", "Note", 330),
        ):
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="center" if column == "amount" else "w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=10)

        bottom = tk.Frame(self, bg="#f8fafc", padx=12, pady=8)
        bottom.pack(fill="x")
        tk.Button(bottom, text="Delete Selected", command=self.delete_selected).pack(side="left")
        tk.Button(bottom, text="Clear All", command=self.clear_all).pack(side="left", padx=8)
        self.total_label = tk.Label(bottom, text="Total: 0.00", bg="#f8fafc", font=("Segoe UI", 13, "bold"))
        self.total_label.pack(side="right")

        self.load_expenses()
        self.refresh_table()

    def add_field(self, parent, label, default, column):
        tk.Label(parent, text=label, bg="#f8fafc").grid(row=0, column=column, sticky="w", padx=(0, 8))
        entry = tk.Entry(parent, width=16)
        entry.insert(0, default)
        entry.grid(row=1, column=column, sticky="w", padx=(0, 8))
        return entry

    def load_expenses(self):
        if DATA_FILE.exists():
            try:
                self.expenses = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.expenses = []

    def save_expenses(self):
        DATA_FILE.write_text(json.dumps(self.expenses, indent=2), encoding="utf-8")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return
        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
            return
        record = {
            "date": self.date_entry.get().strip() or dt.date.today().isoformat(),
            "category": self.category_entry.get().strip() or "General",
            "amount": round(amount, 2),
            "note": self.note_entry.get().strip(),
        }
        self.expenses.append(record)
        self.amount_entry.delete(0, "end")
        self.note_entry.delete(0, "end")
        self.save_expenses()
        self.refresh_table()

    def delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            return
        index = self.tree.index(selection[0])
        del self.expenses[index]
        self.save_expenses()
        self.refresh_table()

    def clear_all(self):
        if messagebox.askyesno("Clear Expenses", "Delete all expense records?"):
            self.expenses.clear()
            self.save_expenses()
            self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0.0
        for expense in self.expenses:
            total += float(expense["amount"])
            self.tree.insert(
                "",
                "end",
                values=(expense["date"], expense["category"], f"{expense['amount']:.2f}", expense["note"]),
            )
        self.total_label.config(text=f"Total: {total:.2f}")


if __name__ == "__main__":
    ExpenseTracker().mainloop()
