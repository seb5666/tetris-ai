from board import Board
from copy import deepcopy
trim_limit = 3

# Calculate the rotation map
b = Board(fileName='test/board1')

b.start()
number_of_board_states = 7 ** b.width
available_actions = [ 'w', 'a', 's', 'd' ]

piece_array = []
for piece in b.pieces:
    for i in range(4):
        piece = deepcopy(piece)
        if piece not in piece_array:
            piece_array.append(piece)
        piece = b.rotatePiece(deepcopy(piece))

q_values = [[[[0 for action in range(len(available_actions))] for column in range(b.width)] for piece_type in range(len(piece_array))] for board_state in range(number_of_board_states)]

def encode_board(board):
    total = 0
    multiplier = 1
    heights = get_heights(board)
    last_height = heights[0]
    for height in heights[1:]:
        difference = height - last_height
        # Reduce down to {-3, -2, ..., 2, 3}
        if difference <= -trim_limit:
            difference = -trim_limit
        elif difference >= trim_limit:
            difference = trim_limit
        # Scale up to {0, 1, 2, ..., 6}
        difference += trim_limit
        total += multiplier * difference
        # print(total)
        multiplier *= 7
        last_height = height
    return total

# Returns the current state of the board in our representation
def get_heights(board):
    heights = [0 for j in range(len(board[0]))]
    for j in range(len(board[0])):
        for i in range(len(board) - 1, -1, -1):
            if board[i][j] > 0:
                heights[j] = i + 1
                break
    return heights

def get_piece_type(board):
    return piece_array.index(board.current_piece)

# for row in b.board:
#     print(row)
# print(number_of_board_states)
print(encode_board(b.board))
print(get_piece_type(b))
print(b.piece_column)
