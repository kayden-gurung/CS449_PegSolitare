from board import Board, validate_size
from game import Game, ManualGame, AutomatedGame
import pytest


# ===== BOARD TESTS =====

# --- AC 1.1: Board updates when a valid size is entered ---

class TestBoardCreation:
    def test_english_default_size(self):
        board = Board(7, "English")
        assert board.rows == 7 and board.cols == 7

    def test_english_different_size(self):
        board = Board(9, "English")
        assert board.rows == 9 and board.cols == 9

    def test_diamond_default_size(self):
        board = Board(7, "Diamond")
        assert board.rows == 7 and board.cols == 7

    def test_hexagon_default_size(self):
        board = Board(5, "Hexagon")
        assert board.rows == 5


# --- AC 1.2: Only valid sizes are accepted ---

class TestValidateSize:
    def test_valid_english_7(self):
        assert validate_size(7, "English") == True

    def test_valid_english_5(self):
        assert validate_size(5, "English") == True

    def test_reject_english_even(self):
        assert validate_size(6, "English") == False

    def test_reject_english_too_small(self):
        assert validate_size(3, "English") == False

    def test_valid_diamond_7(self):
        assert validate_size(7, "Diamond") == True

    def test_reject_diamond_even(self):
        assert validate_size(6, "Diamond") == False

    def test_valid_hex_5(self):
        assert validate_size(5, "Hexagon") == True

    def test_valid_hex_7(self):
        assert validate_size(7, "Hexagon") == True

    def test_reject_hex_too_small(self):
        assert validate_size(3, "Hexagon") == False

    def test_reject_hex_even(self):
        assert validate_size(6, "Hexagon") == False


# --- AC 1.3: Board type selection ---

class TestBoardType:
    def test_english_is_cross_shaped(self):
        board = Board(7, "English")
        assert board.grid[0][0] == -1
        assert board.grid[0][1] == -1
        for c in range(7):
            assert board.grid[3][c] != -1

    def test_diamond_is_diamond_shaped(self):
        board = Board(7, "Diamond")
        assert board.grid[0][0] == -1
        assert board.grid[0][6] == -1
        assert board.grid[0][3] == 1
        for c in range(7):
            assert board.grid[3][c] != -1

    def test_hexagon_has_valid_cells(self):
        board = Board(5, "Hexagon")
        assert board.peg_count() == 18


# --- AC 1.4: Correct layout with center hole ---

class TestBoardLayout:
    def test_english_center_empty(self):
        assert Board(7, "English").grid[3][3] == 0

    def test_diamond_center_empty(self):
        assert Board(7, "Diamond").grid[3][3] == 0

    def test_hexagon_center_empty(self):
        board = Board(5, "Hexagon")
        holes = [(r, c) for r in range(board.rows)
                 for c in range(board.cols) if board.grid[r][c] == 0]
        assert len(holes) == 1

    def test_english_peg_count(self):
        assert Board(7, "English").peg_count() == 32

    def test_diamond_peg_count(self):
        assert Board(7, "Diamond").peg_count() == 24


# --- AC 2.1: Valid move via Board ---

class TestBoardMove:
    def test_valid_move_succeeds(self):
        board = Board(7, "English")
        assert board.make_move(1, 3, 3, 3) == True

    def test_peg_moves_to_destination(self):
        board = Board(7, "English")
        board.make_move(1, 3, 3, 3)
        assert board.grid[3][3] == 1

    def test_source_becomes_empty(self):
        board = Board(7, "English")
        board.make_move(1, 3, 3, 3)
        assert board.grid[1][3] == 0

    def test_jumped_peg_removed(self):
        board = Board(7, "English")
        board.make_move(1, 3, 3, 3)
        assert board.grid[2][3] == 0

    def test_invalid_move_rejected(self):
        board = Board(7, "English")
        assert board.make_move(0, 3, 2, 3) == False

    def test_hex_has_6_directions(self):
        board = Board(5, "Hexagon")
        moves = board.get_valid_moves()
        dirs = set()
        for fr, fc, tr, tc in moves:
            fq, frr = board._offset_to_cube(fr, fc)
            tq, trr = board._offset_to_cube(tr, tc)
            dirs.add((tq - fq, trr - frr))
        assert len(dirs) > 4


# ===== GAME HIERARCHY TESTS =====

# --- Game base class ---

class TestGameBase:
    def test_game_creates_board(self):
        game = Game(7, "English")
        assert game.board is not None
        assert game.board.peg_count() == 32

    def test_game_tracks_move_history(self):
        game = Game(7, "English")
        game.make_move(1, 3, 3, 3)
        assert len(game.move_history) == 1
        assert game.move_history[0] == (1, 3, 3, 3)

    def test_game_invalid_move_no_history(self):
        game = Game(7, "English")
        game.make_move(0, 3, 2, 3)
        assert len(game.move_history) == 0

    def test_game_not_over_at_start(self):
        game = Game(7, "English")
        assert game.is_game_over() == False
        assert game.has_won() == False

    def test_game_over_one_peg(self):
        game = Game(7, "English")
        for r in range(game.board.rows):
            for c in range(game.board.cols):
                if game.board.grid[r][c] == 1:
                    game.board.grid[r][c] = 0
        game.board.grid[3][3] = 1
        assert game.is_game_over() == True
        assert game.has_won() == True

    def test_new_game_resets(self):
        game = Game(7, "English")
        game.make_move(1, 3, 3, 3)
        game.new_game()
        assert game.board.peg_count() == 32
        assert len(game.move_history) == 0

    def test_randomize_board(self):
        game = Game(7, "English")
        game.randomize_board()
        assert game.board.peg_count() < 32
        assert len(game.move_history) == 0

    def test_randomize_has_valid_moves(self):
        game = Game(7, "English")
        game.randomize_board()
        assert len(game.get_valid_moves()) > 0

    def test_randomize_all_board_types(self):
        for bt in ("English", "Diamond", "Hexagon"):
            game = Game(7, bt)
            game.randomize_board()
            assert game.board.peg_count() < game.board.rows * game.board.cols
            assert len(game.get_valid_moves()) > 0













# --- ManualGame ---

class TestManualGame:
    def test_is_subclass_of_game(self):
        assert issubclass(ManualGame, Game)

    def test_select_peg(self):
        game = ManualGame(7, "English")
        assert game.select_peg(0, 3) == True
        assert game.selected == (0, 3)

    def test_select_empty_fails(self):
        game = ManualGame(7, "English")
        assert game.select_peg(3, 3) == False
        assert game.selected is None

    def test_attempt_move_success(self):
        game = ManualGame(7, "English")
        game.select_peg(1, 3)
        result = game.attempt_move(3, 3)
        assert result == "moved"
        assert game.board.grid[3][3] == 1
        assert game.selected is None

    def test_attempt_move_reselect(self):
        game = ManualGame(7, "English")
        game.select_peg(1, 3)
        result = game.attempt_move(0, 3)
        assert result == "reselected"
        assert game.selected == (0, 3)

    def test_attempt_move_invalid(self):
        game = ManualGame(7, "English")
        game.select_peg(1, 3)
        result = game.attempt_move(0, 0)
        assert result == "invalid"
        assert game.selected is None

    def test_new_game_clears_selection(self):
        game = ManualGame(7, "English")
        game.select_peg(1, 3)
        game.new_game()
        assert game.selected is None







# --- AutomatedGame ---

class TestAutomatedGame:
    def test_is_subclass_of_game(self):
        assert issubclass(AutomatedGame, Game)

    def test_play_next_move_returns_tuple(self):
        game = AutomatedGame(7, "English")
        move = game.play_next_move()
        assert move is not None
        assert len(move) == 4

    def test_play_next_move_changes_board(self):
        game = AutomatedGame(7, "English")
        game.play_next_move()
        assert game.board.peg_count() == 31

    def test_play_next_move_records_history(self):
        game = AutomatedGame(7, "English")
        game.play_next_move()
        assert len(game.move_history) == 1

    def test_play_until_game_over(self):
        game = AutomatedGame(7, "English")
        moves = 0
        while not game.is_game_over():
            result = game.play_next_move()
            if result is None:
                break
            moves += 1
        assert game.is_game_over() == True
        assert moves == len(game.move_history)

    def test_play_next_move_returns_none_when_over(self):
        game = AutomatedGame(7, "English")
        # clear board to 1 peg
        for r in range(game.board.rows):
            for c in range(game.board.cols):
                if game.board.grid[r][c] == 1:
                    game.board.grid[r][c] = 0
        game.board.grid[3][3] = 1
        game._game_over = True
        assert game.play_next_move() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
