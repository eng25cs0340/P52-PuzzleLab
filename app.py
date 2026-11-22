
import streamlit as st
from puzzle_generator import generate_puzzle, count_solutions
from csp.solver import solve_sudoku
from validator import validate_sudoku, preserves_clues
from agent.workflow import get_hint
from evaluation.metrics import calculate_metrics

st.set_page_config(
    page_title="P52 PuzzleLab",
    page_icon="🧩",
    layout="wide"
)

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5edff, #e0edff);
    color: #252052;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312e81, #581c87);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, h4, p, label {
    color: #252052;
}

.hero {
    background: linear-gradient(110deg, #7c3aed, #2563eb);
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 8px 20px #4338ca30;
}

.hero h1, .hero p {
    color: white !important;
}

.hero h1 {
    font-size: 38px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #ddd6fe;
    margin-bottom: 18px;
    box-shadow: 0 5px 15px #4338ca15;
}

.section-title {
    color: #6d28d9 !important;
    font-size: 25px;
    font-weight: 800;
    margin-top: 15px;
    margin-bottom: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #5b21b6, #1d4ed8);
    color: white !important;
    border: 2px solid #c4b5fd;
}

.stTextArea textarea {
    background: white !important;
    color: #252052 !important;
    border: 2px solid #a78bfa !important;
    border-radius: 12px !important;
}

.metric-card {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border-radius: 16px;
    padding: 20px 10px;
    text-align: center;
    box-shadow: 0 5px 15px #4338ca25;
}

.metric-card h2, .metric-card p {
    color: white !important;
    margin: 0;
}

.metric-card h2 {
    font-size: 32px;
}

.board {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    max-width: 540px;
    margin: 15px auto;
    border: 3px solid #6d28d9;
    border-radius: 8px;
    overflow: hidden;
}

.cell {
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    color: #312e81 !important;
    border: 1px solid #c4b5fd;
    font-size: 19px;
    font-weight: bold;
}

.cell:nth-child(3n) {
    border-right: 3px solid #7c3aed;
}

.cell:nth-child(9n) {
    border-right: none;
}

.cell:nth-child(n+19):nth-child(-n+27),
.cell:nth-child(n+46):nth-child(-n+54) {
    border-bottom: 3px solid #7c3aed;
}

.stAlert p {
    color: #252052 !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🧩 P52 - PUZZLELAB</h1>
    <p>✨ Puzzle Generator and Solver Tutor ✨</p>
    <p>GENERATE • SOLVE • LEARN • IMPROVE</p>
</div>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "puzzle" not in st.session_state:
    st.session_state.puzzle = None

if "solution" not in st.session_state:
    st.session_state.solution = None

if "stats" not in st.session_state:
    st.session_state.stats = {
        "generated": 0,
        "unique": 0,
        "solved": 0,
        "hints": 0,
        "validated": 0
    }

if "solved_board" not in st.session_state:
    st.session_state.solved_board = None

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎮 PUZZLE MENU")
    st.markdown("---")

    clues = st.slider(
        "Select Puzzle Difficulty",
        min_value=25,
        max_value=45,
        value=30
    )

    st.markdown("---")
    st.subheader("📚 Project Features")
    st.write("🎲 Puzzle Generation")
    st.write("🧠 CSP Backtracking")
    st.write("💡 AI Tutor Hints")
    st.write("✅ Answer Validation")
    st.write("📊 Performance Metrics")

    st.markdown("---")
    st.caption("P52 | PuzzleLab")


# ---------------- BOARD DISPLAY ----------------
def show_board(board):
    html = '<div class="board">'

    for row in board:
        for number in row:
            value = str(number) if number else "·"
            html += f'<div class="cell">{value}</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


# ---------------- GENERATE PUZZLE ----------------
st.markdown(
    '<div class="section-title">🎲 Sudoku Puzzle Generator</div>',
    unsafe_allow_html=True
)

if st.button("🎲 GENERATE NEW PUZZLE"):
    puzzle, solution = generate_puzzle(clues=clues)

    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.stats["generated"] += 1

    if count_solutions([row[:] for row in puzzle], limit=2) == 1:
        st.session_state.stats["unique"] += 1

    st.session_state.solved_board = None
    st.session_state.last_hint = None
    st.session_state.answer_text = ""

if st.session_state.puzzle is None:
    st.info("👆 Click Generate New Puzzle to begin!")

else:

    # ---------------- PUZZLE AND TUTOR ----------------
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧩 Your Sudoku Puzzle")
        show_board(st.session_state.puzzle)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🤖 AI Puzzle Tutor")
        st.write("Need help? Ask your AI tutor for a hint.")

        if st.button("💡 GIVE ME A HINT"):
            hint = get_hint(st.session_state.puzzle)
            st.session_state.last_hint = hint

            if hint:
                st.session_state.stats["hints"] += 1

        hint = st.session_state.last_hint

        if hint:
            st.success(
                f"Try **{hint['number']}** at row "
                f"**{hint['row']}**, column **{hint['column']}**."
            )
            st.write(hint["explanation"])
        elif hint is not None:
            st.info("No hint is available.")

        st.markdown('</div>', unsafe_allow_html=True)


    # ---------------- SOLVER ----------------
    st.markdown(
        '<div class="section-title">🧠 Sudoku Solver</div>',
        unsafe_allow_html=True
    )

    if st.button("🧠 SOLVE COMPLETE PUZZLE"):
        board = [row[:] for row in st.session_state.puzzle]

        if solve_sudoku(board):
            st.session_state.solved_board = board
            st.session_state.stats["solved"] += 1
        else:
            st.error("This puzzle has no solution.")

    if st.session_state.solved_board is not None:
        st.success("🎉 Puzzle solved successfully!")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        show_board(st.session_state.solved_board)
        st.markdown('</div>', unsafe_allow_html=True)


    # ---------------- VALIDATION ----------------
    st.markdown(
        '<div class="section-title">✅ Answer Validation</div>',
        unsafe_allow_html=True
    )

    st.write("Enter 9 rows with 9 numbers in each row. Use 0 for blanks.")

    answer_text = st.text_area(
        "Your Sudoku Answer",
        key="answer_text",
        height=190,
        placeholder="5 3 0 0 7 0 0 0 0"
    )

    if st.button("✅ VALIDATE MY ANSWER"):

        try:
            rows = [
                [int(x) for x in line.replace(",", " ").split()]
                for line in answer_text.strip().splitlines()
                if line.strip()
            ]

            if len(rows) != 9 or any(len(row) != 9 for row in rows):
                st.error("Enter exactly 9 rows with 9 numbers each.")

            elif any(n < 0 or n > 9 for row in rows for n in row):
                st.error("Only numbers from 0 to 9 are allowed.")

            elif not preserves_clues(st.session_state.puzzle, rows):
                st.error("Do not change the original puzzle clues.")

            elif not validate_sudoku(rows, complete=True):
                st.error("The Sudoku is incomplete or contains repeated numbers.")

            elif rows == st.session_state.solution:
                st.success("🏆 Correct! Excellent work!")
                st.session_state.stats["validated"] += 1

            else:
                st.error("Incorrect solution. Keep trying!")

        except ValueError:
            st.error("Please enter numbers only, separated by spaces.")


# ---------------- PERFORMANCE DASHBOARD ----------------
st.markdown("---")

st.markdown(
    '<div class="section-title">📊 Project Performance Dashboard</div>',
    unsafe_allow_html=True
)

m = calculate_metrics(st.session_state.stats)

a, b, c, d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="metric-card">
        <h2>{m['generated']}</h2>
        <p>🎲 Generated</p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="metric-card">
        <h2>{m['unique']}</h2>
        <p>⭐ Unique Puzzles</p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="metric-card">
        <h2>{m['solved']}</h2>
        <p>🧠 Solved</p>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="metric-card">
        <h2>{m['hints']}</h2>
        <p>💡 Hints Used</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px;">
    <h3 style="color:#6d28d9;">💜 P52 PuzzleLab 💙</h3>
    <p>AI Puzzle Learning System | Learn Through Logic</p>
</div>
""", unsafe_allow_html=True)
