import streamlit as st
import numpy as np
import torch

from Minimax_TTT import Minimax_TicTacToe
from TTTNet import TicTacToeNet


PLAYER   = 'X'  # Human player
COMPUTER = 'O'  # AI player
EMPTY    = ' '  # Empty cell
EOG      = False



# Initialize session state for the board
if "board" not in st.session_state:
    st.session_state.board = -1*np.ones((3, 3))
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.EOG = False



# Title
st.title("Tic-Tac-Toe NN")


st.markdown("""
<style>
/* Make all buttons square and larger */
.stButton > button {
    height: 100px !important;
    width: 100px !important;
    font-size: 2.5rem !important;
    border-radius: 12px !important;
    border: 2px solid #333 !important;
    margin: 1px !important;
    background-color: #f7f7f7 !important;
    transition: background 0.2s, color 0.2s;
}

/* Add hover effect */
.stButton > button:hover {
    background-color: #e0e0e0 !important;
    color: #1976d2 !important;
    border-color: #1976d2 !important;
}

/* Optional: Different color for X and O */
.tic-x {
    color: #1976d2 !important; /* Blue for X */
}
.tic-o {
    color: #d32f2f !important; /* Red for O */
}

.stButton {
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="column"] {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# Display the game board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        with cols[j]:
            cell_value = st.session_state.board[i, j]
            # button_label = ":green[X]" if cell_value == 1 else ":red[O]" if cell_value == 0 else "  "
            button_label = "### :blue[❌]" if cell_value == 1 else "### :red[⭕]" if cell_value == 0 else "###  "
            
            st.button(button_label, key=f"{i}{j}", use_container_width=True, on_click=lambda i=i, j=j: play_game(i, j))



with st.form("board_input_form"):
    vector_str = st.text_input(
        "Enter board as 9 comma-separated values (1 for X, 0 for O, -1 for empty):",
        value=",".join(str(int(x)) for x in st.session_state.board.flatten())
    )
    submitted = st.form_submit_button("Set Board")
    if submitted:
        try:
            vector = [int(x.strip()) for x in vector_str.split(",")]
            if len(vector) == 9 and all(x in [1, 0, -1] for x in vector):
                st.session_state.board = np.array(vector).reshape((3, 3))
            else:
                st.error("Please enter exactly 9 values, each being 1, 0, or -1.")
        except Exception as e:
            st.error("Invalid input. Please enter 9 comma-separated integers (1, 0, or -1).")
