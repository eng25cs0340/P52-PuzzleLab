def is_valid(board, row, col, num):
    if any(board[row][c] == num for c in range(9)):
        return False
    if any(board[r][col] == num for r in range(9)):
        return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == num:
                return False
    return True

def solve_sudoku(board, randomize=False):
    """Solve board in place. Returns True if solved, otherwise False."""
    best = None
    best_options = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                options = [n for n in range(1, 10) if is_valid(board, r, c, n)]
                if not options:
                    return False
                if best_options is None or len(options) < len(best_options):
                    best, best_options = (r, c), options
    if best is None:
        return True
    if randomize:
        import random
        random.shuffle(best_options)
    r, c = best
    for n in best_options:
        board[r][c] = n
        if solve_sudoku(board, randomize=randomize):
            return True
        board[r][c] = 0
    return False
