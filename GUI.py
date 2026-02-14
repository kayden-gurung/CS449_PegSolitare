import tkinter as tk


class SimpleGUIDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sprint 0 GUI Demo")
        self.root.geometry("420x260")

        # variable for checkbox anfd radio buttons
        self.record_game = tk.BooleanVar(value=False)
        self.board_type = tk.StringVar(value="English")

        self._build_ui()

    def _build_ui(self):
        # test
        title = tk.Label(self.root, text="GUI Demo (Text + Lines + Checkbox + Radio Buttons)",
        font=("Segoe UI", 10, "bold"))
        title.pack(pady=10)

        # lines
        canvas = tk.Canvas(self.root, width=380, height=60, bg="white", highlightthickness=1)
        canvas.pack()
        canvas.create_line(20, 15, 360, 15, width=2)   # line 1
        canvas.create_line(20, 45, 360, 45, width=2)   # line 2

        # checkbox
        checkbox = tk.Checkbutton(self.root, text="Record game", variable=self.record_game,
        command=self._update_status)
        checkbox.pack(anchor="w", padx=20, pady=(10, 0))

        # radio buttons
        tk.Label(self.root, text="Board Type:").pack(anchor="w", padx=20, pady=(10, 0))

        rb1 = tk.Radiobutton(self.root, text="English", variable=self.board_type, value="English",
        command=self._update_status)
        rb2 = tk.Radiobutton(self.root, text="Hexagon", variable=self.board_type, value="Hexagon",
        command=self._update_status)
        rb3 = tk.Radiobutton(self.root, text="Diamond", variable=self.board_type, value="Diamond",
        command=self._update_status)

        rb1.pack(anchor="w", padx=40)
        rb2.pack(anchor="w", padx=40)
        rb3.pack(anchor="w", padx=40)

        # status update
        self.status = tk.Label(self.root, text="Status: Ready")
        self.status.pack(pady=10)

    def _update_status(self):
        rec = "ON" if self.record_game.get() else "OFF"
        bt = self.board_type.get()
        self.status.config(text=f"Status: Record={rec}, Board={bt}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleGUIDemo()
    app.run()