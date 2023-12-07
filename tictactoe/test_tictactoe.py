from tictactoe import initial_state, player, actions, result, printBoard, winner, terminal, utility, minimax

X = "X"
O = "O"
EMPTY = None

board =  initial_state()

# print(player(board))
# print(actions(board))

# board = [[X, EMPTY, EMPTY],
#          [EMPTY, O, EMPTY],
#          [EMPTY, EMPTY, EMPTY]]

# print(player(board))
# print(actions(board))
# printBoard(board)
# printBoard(result(board, (1,0)))


# board = [[X, EMPTY, O],
#          [X, O, EMPTY],
#          [X, EMPTY, EMPTY]]
# print("\nWin Test:")
# printBoard(board)
# print(winner(board))

# print("\nTerminal test")
# board = [[X, O, X],
#          [X, O, O],
#          [O, X, X]]
# print(terminal(board))

# print("\nUtility Test: ")
# board = [[X, X, O],
#          [X, O, O],
#          [O, X, O]]
# print(utility(board))

print("\nMinimax Test1: ")
# board = [[X, X, O],
#          [X, O, O],
#          [EMPTY, EMPTY, X]]
board = [[X, EMPTY, EMPTY],
         [EMPTY, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
print(player(board))
print(terminal(board))
print(minimax(board))

print("\nMinimax Test2: ")
board = [[X, EMPTY, EMPTY],
         [X, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
print(player(board))
print(terminal(board))
print(minimax(board))

print("\nMinimax Test3: ")
board = [[X, EMPTY, EMPTY],
         [X, O, EMPTY],
         [O, EMPTY, EMPTY]]
print(player(board))
print(terminal(board))
print(minimax(board))

print("\nMinimax Test4: ")
board = [[X, EMPTY, X],
         [X, O, EMPTY],
         [O, EMPTY, EMPTY]]
print(player(board))
print(terminal(board))
print(minimax(board))

print("\nMinimax Test5: ")
board = [[X, O, X],
         [X, O, EMPTY],
         [O, O, EMPTY]]
print(player(board))
print(terminal(board))
print(minimax(board))