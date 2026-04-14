import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, Toplevel, Text, Button, Scrollbar, RIGHT, Y, BOTH
from board import validate_size
from game import ManualGame, AutomatedGame
import replay 






class SimpleGUIDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Peg Solitaire")
        self.root.geometry("520x780")



        # variables for controls
        self.record_game = tk.BooleanVar(value=False)
        self.board_type = tk.StringVar(value="English")
        self.game_mode = tk.StringVar(value="Manual")
        self.board_size = 7


        # game object, starts as ManualGame
        self.game = ManualGame(self.board_size, "English")

        self._auto_job = None
        self._replay_job = None
        self._start_grid = None

        self._build_ui()
        self._draw_board()
        self._snapshot_start_grid()  # initial snapshot for the default game

    def _build_ui(self):
        # title
        title = tk.Label(self.root, text="Peg Solitaire", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        # top controls frame
        controls_top = tk.Frame(self.root)
        controls_top.pack(pady=(0, 5))

        # board size entry
        tk.Label(controls_top, text="Board Size:").pack(side="left", padx=(20, 5))
        self.size_entry = tk.Entry(controls_top, width=5)
        self.size_entry.insert(0, str(self.board_size))
        self.size_entry.pack(side="left")
        apply_btn = tk.Button(controls_top, text="Apply", command=self._apply_size)
        apply_btn.pack(side="left", padx=5)

        # new game button
        new_game_btn = tk.Button(controls_top, text="New Game", command=self._new_game)
        new_game_btn.pack(side="left", padx=5)

        # randomize button
        self.randomize_btn = tk.Button(controls_top, text="Randomize", command=self._randomize)
        self.randomize_btn.pack(side="left", padx=5)

        # load replay button
        self.load_replay_btn = tk.Button(controls_top, text="Load Replay…", command=self._load_replay_dialog)
        self.load_replay_btn.pack(side="left", padx=5)

        # canvas, board drawn between the two lines
        self.canvas = tk.Canvas(self.root, width=480, height=480, bg="white", highlightthickness=1)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # options frame
        options = tk.Frame(self.root)
        options.pack(pady=5, fill="x")

        # left column, game mode
        left = tk.Frame(options)
        left.pack(side="left", padx=20, anchor="n")

        tk.Label(left, text="Game Mode:").pack(anchor="w")
        for name in ("Manual", "Automated"):
            rb = tk.Radiobutton(left, text=name, variable=self.game_mode, value=name, command=self._on_mode_change)
            rb.pack(anchor="w", padx=20)

        # middle column, board type
        middle = tk.Frame(options)
        middle.pack(side="left", padx=20, anchor="n")

        tk.Label(middle, text="Board Type:").pack(anchor="w")
        for name in ("English", "Hexagon", "Diamond"):
            rb = tk.Radiobutton(middle, text=name, variable=self.board_type, value=name, command=self._on_board_type_change)
            rb.pack(anchor="w", padx=20)

        # right column, checkbox
        right = tk.Frame(options)
        right.pack(side="left", padx=20, anchor="n")

        checkbox = tk.Checkbutton(right, text="Record game", variable=self.record_game)
        checkbox.pack(anchor="w")

        # status
        self.status = tk.Label(self.root, text="Status: Ready")
        self.status.pack(pady=10)



    # drawing

    def _draw_board(self):
        self.canvas.delete("all")
        if self.game.board.board_type == "Hexagon":
            self._draw_hex_board()
        else:
            self._draw_square_board()

    def _draw_square_board(self):
        canvas_w = 480
        grid_size = max(self.game.board.rows, self.game.board.cols)
        cell_size = min(60, (canvas_w - 40) // grid_size)
        board_px = grid_size * cell_size
        offset = (canvas_w - board_px) // 2
        line_pad = 15

        self._cell_size = cell_size
        self._offset = offset

        self.canvas.create_line(20, offset - line_pad, canvas_w - 20, offset - line_pad, width=2)
        self.canvas.create_line(20, offset + board_px + line_pad, canvas_w - 20, offset + board_px + line_pad, width=2)

        pad = 6
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                val = self.game.board.grid[r][c]
                if val == -1:
                    continue
                x1 = offset + c * cell_size + pad
                y1 = offset + r * cell_size + pad
                x2 = offset + (c + 1) * cell_size - pad
                y2 = offset + (r + 1) * cell_size - pad

                fill, outline = self._get_cell_colors(r, c, val)
                self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=2)

    def _draw_hex_board(self):
        canvas_w = 480
        canvas_h = 480

        row_height = 0.866
        total_visual_h = self.game.board.rows * row_height + 0.134
        total_visual_w = self.game.board.cols + 0.5

        cell_size = min(50, (canvas_w - 60) / total_visual_w, (canvas_h - 60) / total_visual_h)

        board_px_w = total_visual_w * cell_size
        board_px_h = total_visual_h * cell_size
        offset_x = (canvas_w - board_px_w) / 2
        offset_y = (canvas_h - board_px_h) / 2
        line_pad = 15

        self._cell_size = cell_size
        self._offset_x = offset_x
        self._offset_y = offset_y

        self.canvas.create_line(20, offset_y - line_pad, canvas_w - 20, offset_y - line_pad, width=2)
        self.canvas.create_line(20, offset_y + board_px_h + line_pad, canvas_w - 20, offset_y + board_px_h + line_pad, width=2)

        radius = cell_size * 0.38
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                val = self.game.board.grid[r][c]
                if val == -1:
                    continue
                cx, cy = self._hex_cell_center(r, c, cell_size, offset_x, offset_y)
                fill, outline = self._get_cell_colors(r, c, val)
                self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=fill, outline=outline, width=2)

    def _hex_cell_center(self, r, c, cell_size, offset_x, offset_y):
        shift = cell_size * 0.5 if r % 2 == 1 else 0
        cx = offset_x + c * cell_size + cell_size / 2 + shift
        cy = offset_y + r * cell_size * 0.866 + cell_size / 2
        return cx, cy

    def _get_cell_colors(self, r, c, val):
        selected = None
        if isinstance(self.game, ManualGame):
            selected = self.game.selected
        if val == 1:
            if selected == (r, c):
                return "#ff8c00", "#cc7000"
            return "#5b3a1a", "#3e2510"
        else:
            return "#d4c4a0", "#8b7340"




    # click handling

    def _on_click(self, event):
        if not isinstance(self.game, ManualGame):
            return  # clicks disabled in automated mode

        row, col = self._pixel_to_cell(event.x, event.y)
        if row is None:
            return
        if self.game.board.grid[row][col] == -1:
            return

        result = self.game.attempt_move(row, col)

        if result == "moved":
            self._draw_board()
            self._check_game_over()
        elif result == "reselected":
            self._draw_board()
            self.status.config(text=f"Status: Selected peg at ({row}, {col})")
        elif result == "invalid":
            self._draw_board()
            self.status.config(text="Status: Invalid move")

    def _pixel_to_cell(self, px, py):
        if self.game.board.board_type == "Hexagon":
            return self._pixel_to_hex(px, py)
        else:
            return self._pixel_to_square(px, py)

    def _pixel_to_square(self, px, py):
        col = int((px - self._offset) // self._cell_size)
        row = int((py - self._offset) // self._cell_size)
        if 0 <= row < self.game.board.rows and 0 <= col < self.game.board.cols:
            return row, col
        return None, None

    def _pixel_to_hex(self, px, py):
        best = None
        best_dist = float("inf")
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                if self.game.board.grid[r][c] == -1:
                    continue
                cx, cy = self._hex_cell_center(r, c, self._cell_size, self._offset_x, self._offset_y)
                dist = (px - cx) ** 2 + (py - cy) ** 2
                if dist < best_dist:
                    best_dist = dist
                    best = (r, c)
        if best and best_dist < (self._cell_size * 0.5) ** 2:
            return best
        return None, None




    # recording helpers

    def _snapshot_start_grid(self):
        """Save a deep copy of the current board grid as the recording's start state."""
        self._start_grid = [row[:] for row in self.game.board.grid]

    # game state

    def _check_game_over(self):
        if self.game.has_won():
            self.status.config(text="Status: YOU WIN!")
            self._show_record_popup()
        elif self.game.is_game_over():
            pegs = self.game.peg_count()
            self.status.config(text=f"Status: Game Over — {pegs} pegs remaining")
            self._show_record_popup()
        else:
            pegs = self.game.peg_count()
            moves = len(self.game.get_valid_moves())
            self.status.config(text=f"Status: {pegs} pegs, {moves} moves available")

    def _show_record_popup(self):
        if not self.record_game.get():
            return
        if not self.game.move_history:
            return

        result = "WIN" if self.game.has_won() else f"LOSS ({self.game.peg_count()} pegs left)"
        mode = "Manual" if isinstance(self.game, ManualGame) else "Automated"

        # Convert 4-tuple history to ((src),(dst)) format for replay module
        moves = [((fr, fc), (tr, tc)) for fr, fc, tr, tc in self.game.move_history]

        content = replay.format_record(
            result=result,
            mode=mode,
            board_type=self.game.board_type,
            size=self.game.size,
            moves=moves,
            start_grid=self._start_grid,
        )

        win = Toplevel(self.root)
        win.title("Game Record")
        win.geometry("400x520")

        sb = Scrollbar(win)
        sb.pack(side=RIGHT, fill=Y)
        txt = Text(win, wrap="word", font=("Consolas", 10), yscrollcommand=sb.set)
        txt.insert("1.0", content)
        txt.config(state="disabled") 
        txt.pack(fill=BOTH, expand=True)
        sb.config(command=txt.yview)

        def save():
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Game Record",
            )
            if path:
                replay.save_record(
                    path=path,
                    result=result,
                    mode=mode,
                    board_type=self.game.board_type,
                    size=self.game.size,
                    moves=moves,
                    start_grid=self._start_grid,
                )

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=4)
        Button(btn_frame, text="Save Record…", command=save).pack(side="left", padx=4)
        Button(btn_frame, text="OK", command=win.destroy).pack(side="left", padx=4)

    # loading a replay

    def _load_replay_dialog(self):
        """Open a .txt replay file and play it back automatically."""
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Replay",
        )
        if not path:
            return

        try:
            meta, start_grid, moves = replay.load_replay(path)
        except Exception as e:
            messagebox.showerror("Load Replay", f"Could not read file:\n{e}")
            return

        if not moves:
            messagebox.showerror("Load Replay", "No moves found in file.")
            return

        # cancel any running automated game or replay
        self._stop_auto()
        self._stop_replay()

        # force manual mode
        self.game_mode.set("Manual")

        # apply board type from file if present
        bt = meta.get("Board", self.board_type.get())
        if bt in ("English", "Hexagon", "Diamond"):
            self.board_type.set(bt)

        # apply size from file if present and valid
        try:
            size = int(meta.get("Size", self.board_size))
            if validate_size(size, bt):
                self.board_size = size
                self.size_entry.delete(0, tk.END)
                self.size_entry.insert(0, str(size))
        except (ValueError, TypeError):
            pass

        # reset to a fresh starting board
        self.game = ManualGame(self.board_size, self.board_type.get())

        if start_grid is not None:
            self.game.board.grid = [row[:] for row in start_grid]

        self._draw_board()
        self.status.config(text=f"Status: Replaying {len(moves)} moves from file…")

        # STRART PLAYBACK
        self._replay_step(moves, 0)

    def _replay_step(self, moves, i):
        """Apply one move from the replay list, then schedule the next."""
        if i >= len(moves):
            self._draw_board()
            self.status.config(text=f"Status: Replay complete ({len(moves)} moves)")
            self._check_game_over()
            return

        (fr, fc), (tr, tc) = moves[i]

        # attempt_move is click-based: first click selects, second click moves.
        # make sure nothing is preselected, then perform the two clicks.
        self.game.selected = None
        self.game.attempt_move(fr, fc)
        move_result = self.game.attempt_move(tr, tc)

        if move_result != "moved":
            messagebox.showerror(
                "Replay Error",
                f"Illegal move at step {i + 1}: ({fr},{fc}) -> ({tr},{tc})\n"
                f"Stopping replay."
            )
            self._draw_board()
            return

        self._draw_board()
        self.status.config(text=f"Status: Replay step {i + 1}/{len(moves)}")
        self._replay_job = self.root.after(500, self._replay_step, moves, i + 1)

    def _stop_replay(self):
        if self._replay_job is not None:
            self.root.after_cancel(self._replay_job)
            self._replay_job = None

    # Automated Game

    def _auto_step(self):
        """Play one automated move, then schedule the next."""
        if not isinstance(self.game, AutomatedGame):
            return
        move = self.game.play_next_move()
        if move:
            self._draw_board()
            pegs = self.game.peg_count()
            moves_left = len(self.game.get_valid_moves())
            self.status.config(text=f"Status: Auto played ({move[0]},{move[1]}) -> ({move[2]},{move[3]}) | {pegs} pegs, {moves_left} moves left")
            self._auto_job = self.root.after(500, self._auto_step)
        else:
            self._draw_board()
            self._check_game_over()

    def _stop_auto(self):
        """Cancel any scheduled automated move."""
        if self._auto_job is not None:
            self.root.after_cancel(self._auto_job)
            self._auto_job = None

    # Controls

    def _new_game(self):
        """Reset with current settings."""
        self._stop_auto()
        self._stop_replay()
        bt = self.board_type.get()
        mode = self.game_mode.get()

        if mode == "Manual":
            self.game = ManualGame(self.board_size, bt)
        else:
            self.game = AutomatedGame(self.board_size, bt)

        self._draw_board()
        self._snapshot_start_grid()  # capture standard starting board
        self.status.config(text="Status: New game started")

        if mode == "Automated":
            self._auto_job = self.root.after(500, self._auto_step)

    def _randomize(self):
        """Randomize the board for manual play."""
        if not isinstance(self.game, ManualGame):
            self.status.config(text="Status: Randomize is only available in Manual mode")
            return
        self.game.randomize_board()

        # Treat randomize as a fresh start: clear move history and snapshot the
        # randomized state so replay starts from here.
        self.game.move_history.clear()
        self._snapshot_start_grid()

        pegs = self.game.peg_count()
        moves = len(self.game.get_valid_moves())
        self._draw_board()
        self.status.config(text=f"Status: Randomized — {pegs} pegs, {moves} moves available")

    def _on_mode_change(self):
        """Handle game mode radio button change."""
        self._new_game()


    def _on_board_type_change(self):
        bt = self.board_type.get()
        if not validate_size(self.board_size, bt):
            self.board_size = 7 if bt != "Hexagon" else 7
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.board_size))
        self._new_game()


    def _apply_size(self):
        bt = self.board_type.get()
        try:
            new_size = int(self.size_entry.get())
            if not validate_size(new_size, bt):
                if bt == "Hexagon":
                    self.status.config(text="Status: Size must be an odd number between 5 and 21")
                else:
                    self.status.config(text="Status: Size must be an odd number between 5 and 21")
                return
            self.board_size = new_size
            self._new_game()
        except ValueError:
            self.status.config(text="Status: Enter a valid number")

    def run(self):
        self.root.mainloop()




if __name__ == "__main__":
    app = SimpleGUIDemo()
    app.run()
