import random
from board import Board, validate_size


class Game:
    # base class for Peg Solitaire games.
    # handles shared logic: board management, move history, game state

    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self.board = Board(size, board_type)
        self.move_history = []
        self._game_over = False

    def new_game(self):
        # erset the board and start a fresh game
        self.board = Board(self.size, self.board_type)
        self.move_history = []
        self._game_over = False

    def make_move(self, from_r, from_c, to_r, to_c):
        # attempt a move. returns True if successful
        if self._game_over:
            return False
        if self.board.make_move(from_r, from_c, to_r, to_c):
            self.move_history.append((from_r, from_c, to_r, to_c))
            if self.is_game_over():
                self._game_over = True
            return True
        return False

    def is_game_over(self):
        # game is over
        return len(self.board.get_valid_moves()) == 0

    def has_won(self):
        return self.board.peg_count() == 1 and self.is_game_over()

    def peg_count(self):
        return self.board.peg_count()

    def get_valid_moves(self):
        return self.board.get_valid_moves()

    def randomize_board(self):
        # randomize the board by making a series of random moves from a fresh state. Retries if the result has no valid moves left
        for _ in range(50):  # retry up to 50 times
            self.new_game()
            num_moves = random.randint(5, 15)
            for _ in range(num_moves):
                moves = self.board.get_valid_moves()
                if not moves:
                    break
                move = random.choice(moves)
                self.board.make_move(*move)
            # check that the player has at least one move
            if self.board.get_valid_moves():
                break
        # clear history since these aren't player moves
        self.move_history = []
        self._game_over = False



class ManualGame(Game):

    def __init__(self, size=7, board_type="English"):
        super().__init__(size, board_type)
        self.selected = None  # (row, col) of currently selected peg

    def new_game(self):
        super().new_game()
        self.selected = None

    def select_peg(self, row, col):
        # select a peg at (row, col)
        if self._game_over:
            return False
        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            if self.board.grid[row][col] == 1:
                self.selected = (row, col)
                return True
        self.selected = None
        return False

    def attempt_move(self, to_r, to_c):
        if self.selected is None:
            # no peg selected — try selecting this cell
            if self.select_peg(to_r, to_c):
                return "reselected"
            return "no_selection"

        from_r, from_c = self.selected

        # try the move
        if self.make_move(from_r, from_c, to_r, to_c):
            self.selected = None
            return "moved"

        # clicked a different peg — reselect
        if self.select_peg(to_r, to_c):
            return "reselected"

        # invalid move
        self.selected = None
        return "invalid"




class AutomatedGame(Game):

    def __init__(self, size=7, board_type="English"):
        super().__init__(size, board_type)

    def play_next_move(self):
        # Play one random valid move. Returns the move tuple or None if game is over
        if self._game_over:
            return None
        moves = self.board.get_valid_moves()
        if not moves:
            self._game_over = True
            return None
        move = random.choice(moves)
        self.make_move(*move)
        return move
