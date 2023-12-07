"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

class Node():
    def __init__(self, state, parent, action):
        self.state =  state
        self.parent = parent
        self.action = action


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
    If the board is in initial state, then return X.
    If there is an odd number of EMPTY squares, then it is X's turn
    If there is an even number of EMPTY squares, then it is O's turn
    Any return value is acceptable if it is a terminal board/state
    """
    num_of_empty = 0
    for i in board:
        for j in i:
            if j == EMPTY:
                num_of_empty += 1
    if num_of_empty%2 == 0:
        return O
    else:
        return X
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    i is the row
    j is the column
    set should be all positions that do not have an X or O in them (Empty)
    """
    available_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                available_actions.add((i,j))
    return available_actions
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    If the action provided is not a valid action, then raise an exception.
    Return the board that would result in taking the action by the player 
    whose turn it is.
    Be sure to make sure that the original board is not modified. Make a deep copy
    of the board.
    """
    available_actions = actions(board)
    if not action in available_actions:
        raise NameError("Action is not valid")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board
    
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Returns X if they won, or O if they won
    Return None if there is no winner yet or a tie
    """
    winning_condition = {((0,0), (0,1), (0,2)),
                      ((1,0), (1,1), (1,2)),
                      ((2,0), (2,1), (2,2)),
                      ((0,0), (1,0), (2,0)),
                      ((0,1), (1,1), (2,1)),
                      ((0,2), (1,2), (2,2)),
                      ((0,0), (1,1), (2,2)),
                      ((2,0), (1,1), (0,2))}
    
    for condition in winning_condition:
        num_of_X_spots = 0
        num_of_O_spots = 0
        for spot in condition:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == X and (i, j) == spot:
                        num_of_X_spots += 1
                    if board[i][j] == O and (i, j) == spot:
                        num_of_O_spots += 1
            if num_of_X_spots == 3:
                return X
            if num_of_O_spots == 3:
                return O
    return None
        
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    if there is a winner, return true
    if there are no available actions, return true
    otherwise, return false
    """
    
    if winner(board):
        return True
    
    if len(actions(board)) == 0:
        return True
    
    return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    if winner(board) == O: return -1
    if winner(board) == None: return 0
    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Returns an action (i, j) for the current player that is of the allowable actions
    If the board is terminal, then return None
    When the player is 0, then you are trying for a score of -1
    When the player is X, then you are trying for a score of 1
    """
    if terminal(board): return None
    
    desired_score = 0
    current_score = 0
    if player(board) == X: 
        desired_score = 1
        current_score = -100
    if player(board) == O: 
        desired_score = -1
        current_score = 100 
    
    available_actions = actions(board)
    selected_action = ()
    for action in available_actions:
        new_board = result(board, action)
        if player(board) == X:
            if current_score < maxValue(new_board):
                current_score = maxValue(new_board)
                selected_action = action
        if player(board) == O:
            if current_score > minValue(new_board):
                current_score = minValue(new_board)
                selected_action = action
    return selected_action

def maxValue(board):
    if terminal(board):
        return utility(board)
    else:
        available_actions = actions(board)
        scores = []
        for action in available_actions:
            scores.append(minValue(result(board, action)))
        return min(scores)

def minValue(board):
    if terminal(board):
        return utility(board)
    else:
        available_actions = actions(board)
        scores = []
        for action in available_actions:
            scores.append(maxValue(result(board, action)))
        return max(scores)

def printBoard(board):
    print("Board Configuration:")
    print(board[0])
    print(board[1])
    print(board[2])
