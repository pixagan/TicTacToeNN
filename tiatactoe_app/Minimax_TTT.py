class Minimax_TicTacToe:

    def __init__(self):

        self.PLAYER   = 'X'  # Human player
        self.COMPUTER = 'O'  # AI player
        self.EMPTY    = ' '  # Empty cell
        self.board    = [' '] * 9


    def is_winner(self, board, player):
        # Check rows, columns, and diagonals
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(board[i] == player for i in pattern) for pattern in win_patterns)


    def is_moves_left(self, board):
        return self.EMPTY in board


    def minimax(self, board, is_maximizing):
        if self.is_winner(board, self.COMPUTER):
            return 10
        if self.is_winner(board, self.PLAYER):
            return -10
        if not self.is_moves_left(board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == self.EMPTY:
                    board[i] = self.COMPUTER
                    score = self.minimax(board, False)
                    board[i] = self.EMPTY
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == self.EMPTY:
                    board[i] = self.PLAYER
                    score = self.minimax(board, True)
                    board[i] = self.EMPTY
                    best_score = min(score, best_score)
            return best_score



    def convert_2d_to_1d(self, board_2d):
        # Flatten the 2D board to 1D
        board_1d = board_2d.flatten()
        
        # Convert to list for easier manipulation
        board_1d = list(board_1d)
        
        # Map the values: -1 -> ' ', 0 -> 'O', 1 -> 'X'
        for i in range(len(board_1d)):
            if board_1d[i] == -1:
                board_1d[i] = self.EMPTY  # EMPTY is already defined as ' ' in your constants
            elif board_1d[i] == 0:
                board_1d[i] = self.COMPUTER  # COMPUTER is already defined as 'O'
            elif board_1d[i] == 1:
                board_1d[i] = self.PLAYER  # PLAYER is already defined as 'X'
        
        return board_1d


    def compute_move_minimax(self, board_in):

        board = self.convert_2d_to_1d(board_in)

        best_score = float('-inf')
        best_move = -1

        for i in range(9):
            if board[i] == self.EMPTY:
                board[i] = self.COMPUTER
                score = self.minimax(board, False)
                board[i] = self.EMPTY
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move






