from board import validate_size, create_english_board
import pytest
 
 
# --- AC 1.1: Board updates when a valid size is entered ---
 
class TestBoardCreation:
    def test_board_created_with_default_size(self):
        board = create_english_board(7)
        assert len(board) == 7
        assert len(board[0]) == 7
 
    def test_board_created_with_different_size(self):
        board = create_english_board(9)
        assert len(board) == 9
        assert len(board[0]) == 9
 
 
# --- AC 1.2: Only odd numbers >= 5 are accepted ---
 
class TestValidateSize:
    def test_valid_size_7(self):
        assert validate_size(7) == True
 
    def test_valid_size_5(self):
        assert validate_size(5) == True
 
    def test_valid_size_9(self):
        assert validate_size(9) == True
 
    def test_reject_even_number(self):
        assert validate_size(6) == False
 
    def test_reject_too_small(self):
        assert validate_size(3) == False
 
    def test_reject_negative(self):
        assert validate_size(-1) == False
 
 
# --- AC 1.3: Board type selection (English only for now) ---
 
class TestBoardType:
    def test_english_board_is_cross_shaped(self):
        board = create_english_board(7)
        # top-left 2x2 corner should be invalid
        assert board[0][0] == -1
        assert board[0][1] == -1
        assert board[1][0] == -1
        assert board[1][1] == -1
        # top-right 2x2 corner should be invalid
        assert board[0][5] == -1
        assert board[0][6] == -1
        assert board[1][5] == -1
        assert board[1][6] == -1
        # middle row should all be valid (pegs or hole)
        for c in range(7):
            assert board[3][c] != -1
 
 
# --- AC 1.4: Correct cross shape with center hole ---
 
class TestBoardLayout:
    def test_center_is_empty(self):
        board = create_english_board(7)
        assert board[3][3] == 0
 
    def test_center_empty_size_9(self):
        board = create_english_board(9)
        assert board[4][4] == 0
 
    def test_non_center_valid_positions_have_pegs(self):
        board = create_english_board(7)
        # spot that should be a peg (not center, not corner)
        assert board[0][3] == 1
        assert board[3][0] == 1
        assert board[6][3] == 1
 
    def test_correct_peg_count_size_7(self):
        board = create_english_board(7)
        pegs = sum(cell == 1 for row in board for cell in row)
        assert pegs == 32  # English board has 32 pegs (33 positions - 1 center)
 
    def test_correct_invalid_count_size_7(self):
        board = create_english_board(7)
        invalid = sum(cell == -1 for row in board for cell in row)
        assert invalid == 16  # four 2x2 corners = 16 invalid cells
 
 
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
