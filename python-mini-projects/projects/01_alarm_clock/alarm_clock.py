"""Alarm Clock mini project using Tkinter."""

import datetime as dt
import threading
import time
import tkinter as tk
from tkinter import messagebox


try:
    import winsound
except ImportError:
    winsound = None


class AlarmClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock")
        self.geometry("420x320")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")

        self.alarm_time = None
        self.alarm_active = False
        self.ringing = False

        tk.Label(self, text="Alarm Clock", font=("Segoe UI", 22, "bold"), bg="#f8fafc").pack(pady=(22, 6))
        self.clock_label = tk.Label(self, text="", font=("Consolas", 28, "bold"), bg="#f8fafc", fg="#0f172a")
        self.clock_label.pack(pady=8)

        form = tk.Frame(self, bg="#f8fafc")
        form.pack(pady=12)
        tk.Label(form, text="Alarm Time", font=("Segoe UI", 11), bg="#f8fafc").grid(row=0, column=0, padx=6)
        self.time_entry = tk.Entry(form, width=12, font=("Consolas", 14), justify="center")
        self.time_entry.insert(0, "07:00")
        self.time_entry.grid(row=0, column=1, padx=6)

        buttons = tk.Frame(self, bg="#f8fafc")
        buttons.pack(pady=10)
        tk.Button(buttons, text="Set Alarm", width=12, command=self.set_alarm).grid(row=0, column=0, padx=6)
        tk.Button(buttons, text="Stop", width=12, command=self.stop_alarm).grid(row=0, column=1, padx=6)

        self.status = tk.Label(self, text="Enter time as HH:MM or HH:MM:SS", font=("Segoe UI", 10), bg="#f8fafc", fg="#475569")
        self.status.pack(pady=8)

        self.update_clock()

    def parse_alarm_time(self, value):
        value = value.strip()
        for pattern in ("%H:%M:%S", "%H:%M"):
            try:
                parsed = dt.datetime.strptime(value, pattern)
                return parsed.time()
            except ValueError:
                pass
        raise ValueError("Please enter time as HH:MM or HH:MM:SS")

    def set_alarm(self):
        try:
            self.alarm_time = self.parse_alarm_time(self.time_entry.get())
        except ValueError as error:
            messagebox.showerror("Invalid Time", str(error))
            return
        self.alarm_active = True
        self.ringing = False
        self.status.config(text=f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')}", fg="#166534")

    def stop_alarm(self):
        self.alarm_active = False
        self.ringing = False
        self.status.config(text="Alarm stopped", fg="#991b1b")

    def update_clock(self):
        now = dt.datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))

        if self.alarm_active and self.alarm_time and not self.ringing:
            if now.strftime("%H:%M:%S") == self.alarm_time.strftime("%H:%M:%S"):
                self.ringing = True
                self.alarm_active = False
                self.status.config(text="Alarm ringing!", fg="#b45309")
                threading.Thread(target=self.play_alert, daemon=True).start()
                messagebox.showinfo("Alarm", "Wake up! Your alarm time has arrived.")

        self.after(1000, self.update_clock)

    def play_alert(self):
        for _ in range(5):
            if winsound:
                winsound.Beep(1000, 400)
            else:
                self.bell()
                time.sleep(0.4)
            time.sleep(0.2)


if __name__ == "__main__":
    AlarmClock().mainloop()
