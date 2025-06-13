"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count > o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_remaining = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions_remaining.add((i, j))
    
    return actions_remaining


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)

    if action not in actions(board):
        raise Exception("Not a valid move")
    
    board_copy[action[0]][action[1]] = player(board)
    return board_copy
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # CHECK IF 3 IN ROW
    for row in board:
        if row[0] != EMPTY and row[0] == row[1] == row[2]:
            return row[0]
    
    # CHECK IF 3 IN COL
    for col in range(3):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    # CHECK IF 3 IN DIAG
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # CHECK IF 3 IN ANTI DIAG
    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 0 if winner(board) == None else 1 if winner(board) == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)

    def max_val(state):
        if terminal(state):
            return utility(state)
        max_eval = float('-inf')
        for action in actions(state):
            max_eval = max(max_eval, min_val(result(state, action)))
        return max_eval
    
    def min_val(state):
        if terminal(state):
            return utility(state)
        min_eval = float('inf')
        for action in actions(state):
            min_eval = min(min_eval, max_val(result(state, action)))
        return min_eval
    
    best_action = None
    
    if current_player == X:
        best_score = float('-inf')
        for action in actions(board):
            score = min_val(result(board, action))
            if score > best_score:
                best_action = action
                best_score = score
    else:
        best_score = float('inf')
        for action in actions(board):
            score = max_val(result(board, action))
            if score < best_score:
                best_action = action
                best_score = score
    
    return best_action