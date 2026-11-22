# P52 – PuzzleLab: Puzzle Generator and Solver Tutor

A beginner-friendly Sudoku puzzle generator, solver, hint tutor, and answer validator built with Python and Streamlit.

## Features
- Generates Sudoku puzzles with a unique solution.
- Solves puzzles using recursive backtracking with a minimum-remaining-values cell choice (CSP-style search).
- Gives one-cell hints with a short explanation; it does not reveal the entire solution as a hint.
- Validates a submitted completed board and checks that original clues were preserved.
- Tracks basic session evaluation metrics.
- Includes generic BFS, DFS, Uniform Cost Search, Greedy Best-First Search, and A* implementations.

## Setup (Windows / VS Code)
1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python -m streamlit run app.py
   ```

## Sudoku answer format
Enter exactly 9 lines, each containing 9 numbers separated by spaces. Use `0` for empty cells. Keep all original clues unchanged.

## Project structure
- `app.py` – Streamlit interface
- `puzzle_generator.py` – randomized generator and uniqueness counter
- `csp/solver.py` – CSP/backtracking Sudoku solver
- `validator.py` – Sudoku rule and clue validation
- `agent/workflow.py` – solve and one-step hint workflow
- `evaluation/metrics.py` – evaluation metric helpers
- `algorithms/` – BFS, DFS, UCS, Greedy, and A*

## Notes
- Search algorithm modules are generic graph-search implementations for educational demonstration; the Sudoku solving engine itself uses CSP/backtracking.
- Session metrics reset when the Streamlit session resets.
- The current hint is a valid next-cell hint, not a full natural-language proof of all deductions.
