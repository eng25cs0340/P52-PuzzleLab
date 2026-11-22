def validate_sudoku(board, complete=False):
    if len(board) != 9 or any(len(row) != 9 for row in board):
        return False
    allowed = set(range(1, 10))
    for row in board:
        vals = [n for n in row if n != 0]
        if any(n not in allowed for n in vals) or len(vals) != len(set(vals)):
            return False
        if complete and set(vals) != allowed:
            return False
    for c in range(9):
        vals = [board[r][c] for r in range(9) if board[r][c] != 0]
        if len(vals) != len(set(vals)):
            return False
        if complete and set(vals) != allowed:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            vals = [board[r][c] for r in range(br, br+3)
                    for c in range(bc, bc+3) if board[r][c] != 0]
            if len(vals) != len(set(vals)):
                return False
            if complete and set(vals) != allowed:
                return False
    return True

def preserves_clues(puzzle, answer):
    return all(puzzle[r][c] == 0 or puzzle[r][c] == answer[r][c]
               for r in range(9) for c in range(9))
