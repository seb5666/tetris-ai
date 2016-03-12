from board import Board

trim_limit = 3

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
        print(difference)
        total += multiplier * difference
        # print(total)
        multiplier *= 7
        last_height = height
    print(total)

# Returns the current state of the board in our representation
def get_heights(board):
    heights = [0 for j in range(len(board[0]))]
    for j in range(len(board[0])):
        for i in range(len(board) - 1, -1, -1):
            if board[i][j] > 0:
                heights[j] = i + 1
                break
    print(heights)
    return heights

def get_piece_type(board):
    for row in board.current_piece:
        for block in row:
            if block != 0:
                return block
    return 0

b = Board(fileName='test/board1')
b.start()
for row in b.board:
    print(row)
# print(b.board)
number_of_board_states = 7 ** b.width
print(number_of_board_states)
print(encode_board(b.board))
print(get_piece_type(b))
print(b.piece_column)
available_actions = [ 'w', 'a', 's', 'd' ]
