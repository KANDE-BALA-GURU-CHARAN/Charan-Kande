"""Attendance Management System mini project using SQLite."""

import csv
import datetime as dt
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


DB_FILE = Path(__file__).with_name("attendance.db")


class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management System")
        self.geometry("720x470")
        self.configure(bg="#f8fafc")
        self.today = dt.date.today().isoformat()
        self.conn = sqlite3.connect(DB_FILE)
        self.create_tables()

        header = tk.Frame(self, bg="#f8fafc", padx=12, pady=12)
        header.pack(fill="x")
        tk.Label(header, text=f"Attendance Date: {self.today}", font=("Segoe UI", 14, "bold"), bg="#f8fafc").pack(side="left")

        form = tk.Frame(self, bg="#f8fafc", padx=12)
        form.pack(fill="x")
        self.name_entry = tk.Entry(form, width=35)
        self.name_entry.pack(side="left", padx=(0, 8))
        tk.Button(form, text="Add Student", command=self.add_student).pack(side="left")

        columns = ("id", "name", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=14)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("status", text="Today Status")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=380)
        self.tree.column("status", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

        buttons = tk.Frame(self, bg="#f8fafc", padx=12, pady=8)
        buttons.pack(fill="x")
        tk.Button(buttons, text="Mark Present", command=lambda: self.mark_attendance("Present")).pack(side="left", padx=4)
        tk.Button(buttons, text="Mark Absent", command=lambda: self.mark_attendance("Absent")).pack(side="left", padx=4)
        tk.Button(buttons, text="Delete Student", command=self.delete_student).pack(side="left", padx=4)
        tk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="right", padx=4)

        self.refresh_table()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                status TEXT NOT NULL,
                UNIQUE(student_id, day),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
            """
        )
        self.conn.commit()

    def add_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a student name.")
            return
        try:
            self.conn.execute("INSERT INTO students(name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate", "This student already exists.")
            return
        self.name_entry.delete(0, "end")
        self.refresh_table()

    def selected_student_id(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Select Student", "Please select a student first.")
            return None
        return self.tree.item(selection[0], "values")[0]

    def mark_attendance(self, status):
        student_id = self.selected_student_id()
        if student_id is None:
            return
        self.conn.execute(
            """
            INSERT INTO attendance(student_id, day, status)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, day) DO UPDATE SET status=excluded.status
            """,
            (student_id, self.today, status),
        )
        self.conn.commit()
        self.refresh_table()

    def delete_student(self):
        student_id = self.selected_student_id()
        if student_id is None:
            return
        if not messagebox.askyesno("Delete Student", "Delete selected student and attendance records?"):
            return
        self.conn.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
        self.conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = """
            SELECT students.id, students.name, COALESCE(attendance.status, 'Not Marked')
            FROM students
            LEFT JOIN attendance
            ON students.id = attendance.student_id AND attendance.day = ?
            ORDER BY students.name
        """
        for row in self.conn.execute(query, (self.today,)):
            self.tree.insert("", "end", values=row)

    def export_csv(self):
        file_path = Path(__file__).with_name(f"attendance_{self.today}.csv")
        rows = [self.tree.item(item, "values") for item in self.tree.get_children()]
        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Student Name", "Status"])
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"Attendance saved to:\n{file_path}")


if __name__ == "__main__":
    AttendanceApp().mainloop()
