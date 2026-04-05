def validate_size(size, board_type="English"):
    # return True if size is valid for the given board type
    if not isinstance(size, int):
        return False
    if board_type == "Hexagon":
        return size >= 5 and size <= 21 and size % 2 != 0
    else:  # English or Diamond
        return size >= 5 and size <= 21 and size % 2 != 0


class Board:
    # handles grid state, valid moves, and move execution. not tracking track game-level concerns like history, win/loss, or game mode

    SQUARE_DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    HEX_AXIAL_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self._hex_offset = 0
        self._hex_col_shift = 0

        if board_type == "English":
            self.grid = self._create_english_board()
        elif board_type == "Diamond":
            self.grid = self._create_diamond_board()
        elif board_type == "Hexagon":
            self.grid = self._create_hex_board()

        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0



    # Board Creation 

    def _create_english_board(self):
        s = self.size
        cutoff = (s - 3) // 2
        grid = []
        for r in range(s):
            row = []
            for c in range(s):
                if (r < cutoff and c < cutoff) or \
                   (r < cutoff and c > s - 1 - cutoff) or \
                   (r > s - 1 - cutoff and c < cutoff) or \
                   (r > s - 1 - cutoff and c > s - 1 - cutoff):
                    row.append(-1)
                else:
                    row.append(1)
            grid.append(row)
        mid = s // 2
        grid[mid][mid] = 0
        return grid

    def _create_diamond_board(self):
        s = self.size
        mid = s // 2
        grid = []
        for r in range(s):
            row = []
            for c in range(s):
                if abs(r - mid) + abs(c - mid) <= mid:
                    row.append(1)
                else:
                    row.append(-1)
            grid.append(row)
        grid[mid][mid] = 0
        return grid

    def _create_hex_board(self):
        n = (self.size + 1) // 2 
        self._hex_offset = n - 1
        num_rows = 2 * n - 1

        valid = set()
        for cr in range(-(n - 1), n):
            q_min = max(-(n - 1), -(n - 1) - cr)
            q_max = min(n - 1, (n - 1) - cr)
            for cq in range(q_min, q_max + 1):
                offset_row = cr + self._hex_offset
                offset_col = cq + (offset_row - (offset_row & 1)) // 2
                valid.add((offset_row, offset_col))

        min_col = min(c for _, c in valid)
        self._hex_col_shift = min_col
        valid = {(r, c - min_col) for r, c in valid}

        max_col = max(c for _, c in valid) + 1
        grid = [[-1] * max_col for _ in range(num_rows)]
        for r, c in valid:
            grid[r][c] = 1

        center_row = self._hex_offset
        center_col = 0 + (center_row - (center_row & 1)) // 2 - self._hex_col_shift
        grid[center_row][center_col] = 0
        return grid

    # hex coordinate helpers

    def _offset_to_cube(self, row, col):
        shifted_col = col + self._hex_col_shift
        cube_r = row - self._hex_offset
        cube_q = shifted_col - (row - (row & 1)) // 2
        return cube_q, cube_r

    def _cube_to_offset(self, cq, cr):
        row = cr + self._hex_offset
        col = cq + (row - (row & 1)) // 2 - self._hex_col_shift
        return row, col





    # Move Logic 

    def is_valid_move(self, from_r, from_c, to_r, to_c):
        if not self._in_bounds(from_r, from_c) or not self._in_bounds(to_r, to_c):
            return False
        if self.grid[from_r][from_c] != 1:
            return False
        if self.grid[to_r][to_c] != 0:
            return False
        mid_r, mid_c = self._get_mid(from_r, from_c, to_r, to_c)
        if mid_r is None:
            return False
        if self.grid[mid_r][mid_c] != 1:
            return False
        return True

    def _get_mid(self, from_r, from_c, to_r, to_c):
        if self.board_type == "Hexagon":
            return self._get_hex_mid(from_r, from_c, to_r, to_c)
        else:
            dr = to_r - from_r
            dc = to_c - from_c
            if (abs(dr) == 2 and dc == 0) or (dr == 0 and abs(dc) == 2):
                return from_r + dr // 2, from_c + dc // 2
            return None, None

    def _get_hex_mid(self, from_r, from_c, to_r, to_c):
        fq, fr = self._offset_to_cube(from_r, from_c)
        tq, tr = self._offset_to_cube(to_r, to_c)
        dq = tq - fq
        dr = tr - fr
        if (dq, dr) in [(2*d[0], 2*d[1]) for d in self.HEX_AXIAL_DIRS]:
            mq = fq + dq // 2
            mr = fr + dr // 2
            mid_row, mid_col = self._cube_to_offset(mq, mr)
            if self._in_bounds(mid_row, mid_col):
                return mid_row, mid_col
        return None, None

    def make_move(self, from_r, from_c, to_r, to_c):
        # Execute a move. Returns True if successful, False if invalid
        if not self.is_valid_move(from_r, from_c, to_r, to_c):
            return False
        mid_r, mid_c = self._get_mid(from_r, from_c, to_r, to_c)
        self.grid[from_r][from_c] = 0
        self.grid[mid_r][mid_c] = 0
        self.grid[to_r][to_c] = 1
        return True

    def get_valid_moves(self):
        moves = []
        if self.board_type == "Hexagon":
            directions = self._get_hex_jump_targets
        else:
            directions = self._get_square_jump_targets

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    for to_r, to_c in directions(r, c):
                        if self.is_valid_move(r, c, to_r, to_c):
                            moves.append((r, c, to_r, to_c))
        return moves

    def _get_square_jump_targets(self, r, c):
        for dr, dc in self.SQUARE_DIRS:
            yield r + dr, c + dc

    def _get_hex_jump_targets(self, r, c):
        fq, fr = self._offset_to_cube(r, c)
        for dq, dr in self.HEX_AXIAL_DIRS:
            tq, tr = fq + 2 * dq, fr + 2 * dr
            to_row, to_col = self._cube_to_offset(tq, tr)
            yield to_row, to_col



    # Queries 
    
    def peg_count(self):
        return sum(cell == 1 for row in self.grid for cell in row)

    def _in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != -1
    
