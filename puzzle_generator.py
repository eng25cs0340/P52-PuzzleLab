import random
from csp.solver import solve_sudoku

def count_solutions(board, limit=2):
    """Count solutions up to limit; board is restored before returning."""
    count = 0
    def search():
        nonlocal count
        if count >= limit:
            return
        empty = None
        best_candidates = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    candidates = [n for n in range(1, 10) if is_valid(board, r, c, n)]
                    if not candidates:
                        return
                    if best_candidates is None or len(candidates) < len(best_candidates):
                        empty, best_candidates = (r, c), candidates
        if empty is None:
            count += 1
            return
        r, c = empty
        for n in best_candidates:
            board[r][c] = n
            search()
            board[r][c] = 0
            if count >= limit:
                return
    from csp.solver import is_valid
    search()
    return count

def generate_puzzle(clues=30):
    """Generate a Sudoku puzzle and its unique solution."""
    board = [[0] * 9 for _ in range(9)]
    # Fill diagonal 3x3 boxes independently.
    for start in (0, 3, 6):
        nums = list(range(1, 10))
        random.shuffle(nums)
        k = 0
        for r in range(start, start + 3):
            for c in range(start, start + 3):
                board[r][c] = nums[k]
                k += 1
    solve_sudoku(board, randomize=True)
    solution = [row[:] for row in board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    target = max(17, min(81, int(clues)))
    remaining = 81
    for r, c in cells:
        if remaining <= target:
            break
        old = board[r][c]
        board[r][c] = 0
        if count_solutions([row[:] for row in board], limit=2) != 1:
            board[r][c] = old
        else:
            remaining -= 1
    return board, solution
