import streamlit as st
from puzzle_generator import generate_puzzle, count_solutions
from csp.solver import solve_sudoku, is_valid
from validator import validate_sudoku, preserves_clues
from agent.workflow import get_hint
from evaluation.metrics import calculate_metrics

st.set_page_config(page_title="P52 PuzzleLab", page_icon="🧩", layout="wide")
st.title("🧩 P52 – PuzzleLab")
st.caption("Puzzle Generator and Solver Tutor")

def show_board(board):
    for row in board:
        st.code("  ".join(str(n) if n else "·" for n in row), language=None)

if "puzzle" not in st.session_state:
    st.session_state.puzzle = None
if "solution" not in st.session_state:
    st.session_state.solution = None
if "stats" not in st.session_state:
    st.session_state.stats = {"generated": 0, "unique": 0, "solved": 0, "hints": 0, "validated": 0}

with st.sidebar:
    st.header("Puzzle settings")
    clues = st.slider("Starting clues", 25, 45, 30)
    st.caption("Fewer clues generally make a puzzle harder.")

if st.button("🎲 Generate Sudoku", type="primary"):
    puzzle, solution = generate_puzzle(clues=clues)
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.stats["generated"] += 1
    if count_solutions([r[:] for r in puzzle], limit=2) == 1:
        st.session_state.stats["unique"] += 1
    st.session_state.user_grid = "\n".join(" ".join(map(str, row)) for row in puzzle)

if st.session_state.puzzle is None:
    st.info("Choose the number of starting clues, then click **Generate Sudoku**.")
else:
    left, right = st.columns(2)
    with left:
        st.subheader("Your puzzle")
        show_board(st.session_state.puzzle)
    with right:
        st.subheader("Tutor")
        st.write("Ask for one hint at a time. The tutor will not reveal the full solution.")
        if st.button("💡 Give me one hint"):
            hint = get_hint(st.session_state.puzzle)
            if hint:
                st.session_state.stats["hints"] += 1
                st.session_state.last_hint = hint
            else:
                st.session_state.last_hint = None
        if "last_hint" in st.session_state:
            if st.session_state.last_hint:
                h = st.session_state.last_hint
                st.success(f"Try **{h['number']}** at row **{h['row']}**, column **{h['column']}**.")
                st.write(h["explanation"])
            else:
                st.info("There are no empty cells or the puzzle has no solution.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧠 Solve puzzle"):
            board = [r[:] for r in st.session_state.puzzle]
            if solve_sudoku(board):
                st.session_state.stats["solved"] += 1
                st.session_state.solved_board = board
            else:
                st.error("This puzzle has no solution.")
        if "solved_board" in st.session_state:
            st.subheader("Completed solution")
            show_board(st.session_state.solved_board)
    with c2:
        st.subheader("Submit your answer")
        st.write("Enter 9 rows, with 9 numbers per row. Use 0 for blank cells.")
        answer_text = st.text_area(
            "Your Sudoku answer",
            key="answer_text",
            height=190,
            placeholder="Example: 5 3 0 0 7 0 0 0 0"
        )
        if st.button("✅ Validate answer"):
            try:
                rows = [[int(x) for x in line.replace(",", " ").split()]
                        for line in answer_text.strip().splitlines() if line.strip()]
                if len(rows) != 9 or any(len(row) != 9 for row in rows):
                    st.error("Please enter exactly 9 rows with 9 numbers in each row.")
                elif any(n < 0 or n > 9 for row in rows for n in row):
                    st.error("Only digits from 0 to 9 are allowed.")
                elif not preserves_clues(st.session_state.puzzle, rows):
                    st.error("Some original clues were changed. Keep all given numbers unchanged.")
                elif not validate_sudoku(rows, complete=True):
                    st.error("The board is incomplete or has repeated/invalid numbers.")
                elif rows == st.session_state.solution:
                    st.success("Correct! Excellent work — you solved the puzzle.")
                    st.session_state.stats["validated"] += 1
                else:
                    st.error("This is a valid-looking attempt, but it is not the generated solution. Keep trying!")
            except ValueError:
                st.error("Please enter numbers only, separated by spaces.")

st.divider()
st.subheader("Project evaluation")
m = calculate_metrics(st.session_state.stats)
a, b, c, d = st.columns(4)
a.metric("Puzzles generated", m["generated"])
b.metric("Unique puzzles", m["unique"])
c.metric("Solved", m["solved"])
d.metric("Hints requested", m["hints"])
st.caption("These are live session metrics. They reset when the Streamlit session is reset.")
st.divider()
st.caption("P52 PuzzleLab | AI Puzzle Learning System")
