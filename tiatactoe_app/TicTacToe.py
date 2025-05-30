import streamlit as st
import numpy as np
import torch

from Minimax_TTT import Minimax_TicTacToe
from TTTNet import TicTacToeNet


PLAYER   = 'X'  # Human player
COMPUTER = 'O'  # AI player
EMPTY    = ' '  # Empty cell
EOG      = False

minimax_ttt = Minimax_TicTacToe()
nn_ttt = TicTacToeNet()
#nn_ttt.load_state_dict(torch.load("TTT_Weights_Overfit.pth"))
nn_ttt.load_state_dict(torch.load("TicTacToeWeight.pth"))



# Initialize session state for the board
if "board" not in st.session_state:
    st.session_state.board = -1*np.ones((3, 3))
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.EOG = False




def computer_move_random(board):

    # Find all empty positions (where value is -1)
    empty_positions = np.where(board == -1)

    # Combine the row and column indices into pairs
    empty_positions = list(zip(empty_positions[0], empty_positions[1]))
    
    if empty_positions:
        # Randomly select one empty position
        row, col = empty_positions[np.random.randint(len(empty_positions))]
        # Make the move (assuming computer uses 0 as its mark)
        board[row, col] = 0



## Playing TicTacToe with Minimax
def compute_move_minimax(board):
    best_move = minimax_ttt.compute_move_minimax(board)
    row = best_move // 3
    col = best_move % 3
    board[row, col] = 0


## Playing TicTacToe with Neural Network
def compute_move_nn(board):

    board_1d = board.flatten()
    board_1d = np.append(board_1d, 0)
    board_1d = torch.tensor(board_1d, dtype=torch.float32)
    board_1d = board_1d.view(1, 10)

    #calling the Neural Network
    output = nn_ttt(board_1d)
    _, best_move = torch.max(output.data, 1)
    row = (best_move-1) // 3
    col = (best_move-1) % 3
    board[row, col] = 0
    


def check_end(board):
    return not (board == -1).any()


# Function to check for a winner
def check_winner(board):

    for row in board:
        if row[0] == row[1] == row[2] and row[0] != -1:
            return row[0]

    for col in board.T:
        if col[0] == col[1] == col[2] and col[0] != -1:
            return col[0]

    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != -1:
        return board[0, 0]

    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != -1:
        return board[0, 2]

    if -1 not in board:
        return None


    return None


def check_status(board):
    #take users input  
    #Check for winner or end game if so end game
    winner = check_winner(st.session_state.board)

    if(winner is not None):
        if(winner == 1):
            st.session_state.winner = 'X'
            return
        else:
            st.session_state.winner = 'O'
            return
    else:
        eog = check_end(st.session_state.board)


    if(eog):
        st.session_state.winner = "Draw"
        return


def play_game(index1, index2):

    if(not st.session_state.EOG):

        #check for valid move
        if(st.session_state.board[index1, index2] != -1):
            return

        st.session_state.board[index1, index2] = 1

        check_status(st.session_state.board)

        compute_move_nn(st.session_state.board)

        check_status(st.session_state.board)



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
    margin: 4px !important;
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

</style>
""", unsafe_allow_html=True)


# Display the game board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        with cols[j]:
            cell_value = st.session_state.board[i, j]
            button_label = "### :blue[❌]" if cell_value == 1 else "### :red[⭕]" if cell_value == 0 else "###  "
            
            st.button(button_label, key=f"{i}{j}", use_container_width=True, on_click=lambda i=i, j=j: play_game(i, j))



# Display status message
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.subheader("It's a Draw! 🎭")
    else:
        st.subheader(f"🎉 Player {st.session_state.winner} Wins!")


# Reset button
if st.button("Restart Game", key="restart_button"):
    st.session_state.board = -1*np.ones((3, 3))
    st.session_state.current_player = "X"
    st.session_state.winner  = None
    st.session_state.EOG = False
