"""Drawing Pad mini project using Tkinter Canvas and mouse events."""

import tkinter as tk
from tkinter import filedialog, messagebox


class DrawingPad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drawing Pad")
        self.geometry("760x560")
        self.configure(bg="#eef2f7")

        self.last_x = None
        self.last_y = None
        self.color = tk.StringVar(value="black")
        self.brush_size = tk.IntVar(value=4)

        toolbar = tk.Frame(self, bg="#dbeafe", padx=10, pady=8)
        toolbar.pack(fill="x")

        tk.Label(toolbar, text="Color", bg="#dbeafe").pack(side="left")
        colors = ("black", "red", "green", "blue", "purple", "orange")
        tk.OptionMenu(toolbar, self.color, *colors).pack(side="left", padx=6)

        tk.Label(toolbar, text="Brush", bg="#dbeafe").pack(side="left", padx=(14, 0))
        tk.Scale(toolbar, from_=1, to=20, orient="horizontal", variable=self.brush_size, length=120, bg="#dbeafe").pack(side="left")

        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side="right", padx=5)
        tk.Button(toolbar, text="Save", command=self.save_canvas).pack(side="right", padx=5)

        self.canvas = tk.Canvas(self, bg="white", cursor="pencil", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.last_x is None or self.last_y is None:
            return
        size = self.brush_size.get()
        self.canvas.create_line(
            self.last_x,
            self.last_y,
            event.x,
            event.y,
            fill=self.color.get(),
            width=size,
            capstyle="round",
            smooth=True,
        )
        self.last_x = event.x
        self.last_y = event.y

    def stop_draw(self, _event):
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript file", "*.ps")],
            title="Save drawing",
        )
        if path:
            self.canvas.postscript(file=path)
            messagebox.showinfo("Saved", f"Drawing saved to:\n{path}")


if __name__ == "__main__":
    DrawingPad().mainloop()
