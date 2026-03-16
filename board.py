def validate_size(size):
    """Return True if size is a valid board size (odd number >= 5)."""
    return isinstance(size, int) and size >= 5 and size % 2 != 0
 
def create_english_board(size):
    """Create the English cross-shaped board. 1=peg, 0=hole, -1=invalid."""
    board = []
    cutoff = (size - 3) // 2
    for r in range(size):
        row = []
        for c in range(size):
            if r < cutoff and c < cutoff:
                row.append(-1)
            elif r < cutoff and c > size - 1 - cutoff:
                row.append(-1)
            elif r > size - 1 - cutoff and c < cutoff:
                row.append(-1)
            elif r > size - 1 - cutoff and c > size - 1 - cutoff:
                row.append(-1)
            else:
                row.append(1)
        board.append(row)
    # center starts empty
    mid = size // 2
    board[mid][mid] = 0
    return board
