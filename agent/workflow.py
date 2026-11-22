from copy import deepcopy
from csp.solver import solve_sudoku

def solve_puzzle(board):
    result = deepcopy(board)
    return result if solve_sudoku(result) else None

def get_hint(board):
    """Return one missing cell only; never reveal the complete solution."""
    solution = solve_puzzle(board)
    if solution is None:
        return None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                number = solution[r][c]
                return {
                    "row": r + 1,
                    "column": c + 1,
                    "number": number,
                    "explanation": (
                        f"That cell is empty. {number} is a candidate that fits "
                        "the row, column, and 3×3 box without repeating a number. "
                        "Use this as a clue, then try the next step yourself."
                    )
                }
    return None
