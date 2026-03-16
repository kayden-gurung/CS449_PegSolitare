import tkinter as tk
from board import create_english_board

class SimpleGUIDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        self.root.geometry("520x700")

        # variables for checkbox and radio buttons
        self.record_game = tk.BooleanVar(value=False)
        self.board_type = tk.StringVar(value="English")
        self.board_size = 7

        # board state from board.py
        self.board = create_english_board(self.board_size)

        self._build_ui()
        self._draw_board()

    def _build_ui(self):
        # title
        title = tk.Label(self.root, text="GUI Demo (Text + Lines + Checkbox + Radio Buttons)",
        font=("Segoe UI", 10, "bold"))
        title.pack(pady=10)

        # board size entry
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=(0, 5))
        tk.Label(size_frame, text="Board Size:").pack(side="left", padx=(20, 5))
        self.size_entry = tk.Entry(size_frame, width=5)
        self.size_entry.insert(0, str(self.board_size))
        self.size_entry.pack(side="left")
        apply_btn = tk.Button(size_frame, text="Apply", command=self._apply_size)
        apply_btn.pack(side="left", padx=5)

        # canvas — board drawn between the two lines
        self.canvas = tk.Canvas(self.root, width=480, height=480, bg="white", highlightthickness=1)
        self.canvas.pack()

        # checkbox
        checkbox = tk.Checkbutton(self.root, text="Record game", variable=self.record_game,command=self._update_status)
        checkbox.pack(anchor="w", padx=20, pady=(10, 0))

        # radio buttons
        tk.Label(self.root, text="Board Type:").pack(anchor="w", padx=20, pady=(10, 0))
        for name in ("English", "Hexagon", "Diamond"):
            rb = tk.Radiobutton(self.root, text=name, variable=self.board_type, value=name, command=self._update_status)
            rb.pack(anchor="w", padx=40)

        # status
        self.status = tk.Label(self.root, text="Status: Ready")
        self.status.pack(pady=10)

    def _draw_board(self):
        """Render the board on the canvas between two horizontal lines."""
        self.canvas.delete("all")

        canvas_w = 480
        cell_size = min(60, (canvas_w - 40) // self.board_size)
        board_px = self.board_size * cell_size
        offset_x = (canvas_w - board_px) // 2
        line_pad = 15

        # top line
        top_line_y = offset_x - line_pad
        self.canvas.create_line(20, top_line_y, canvas_w - 20, top_line_y, width=2)

        # bottom line
        bot_line_y = offset_x + board_px + line_pad
        self.canvas.create_line(20, bot_line_y, canvas_w - 20, bot_line_y, width=2)

        # draw pegs and holes
        pad = 6
        for r in range(self.board_size):
            for c in range(self.board_size):
                val = self.board[r][c]
                if val == -1:
                    continue

                x1 = offset_x + c * cell_size + pad
                y1 = offset_x + r * cell_size + pad
                x2 = offset_x + (c + 1) * cell_size - pad
                y2 = offset_x + (r + 1) * cell_size - pad

                if val == 1:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="#5b3a1a", outline="#3e2510", width=2)
                elif val == 0:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="#d4c4a0", outline="#8b7340", width=2)

    def _apply_size(self):
        """Read the size entry, rebuild and redraw the board."""
        try:
            new_size = int(self.size_entry.get())
            if new_size < 5 or new_size % 2 == 0:
                self.status.config(text="Status: Size must be an odd number >= 5")
                return
            self.board_size = new_size
            self.board = create_english_board(self.board_size)
            self._draw_board()
            self._update_status()
        except ValueError:
            self.status.config(text="Status: Enter a valid number")

    def _update_status(self):
        rec = "ON" if self.record_game.get() else "OFF"
        bt = self.board_type.get()
        self.status.config(text=f"Status: Record={rec}, Board={bt}, Size={self.board_size}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleGUIDemo()
    app.run()


if __name__ == "__main__":
    app = SimpleGUIDemo()
    app.run()
