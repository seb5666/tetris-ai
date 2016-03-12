import random
from copy import deepcopy
from boardthread import BoardThread

#TODO: there might be some race condition between making the current piece fall and moving the piece due to user input...
#This should be fixable by adding a mutex, but not sure if actually needed. CHECK THIS!

# Set to true for more debug information
class Board:
    # O piece
    # x x
    # x x
    o_piece = [[1, 1], [1, 1]]

    # Z piece
    # x x ~
    # ~ x x
    z_piece = [[2, 2, 0], [0, 2, 2]]

    # S piece
    # ~ x x
    # x x ~
    s_piece = [[0, 3, 3], [3, 3, 0]]

    # L piece
    # x ~ ~
    # x x x
    l_piece = [[4, 4, 4], [4, 0, 0]]

    # J piece
    # x x x
    # ~ ~ x
    j_piece = [[5, 5, 5], [0, 0, 5]]

    # L piece
    # x x x
    # ~ x ~
    t_piece = [[6, 6, 6], [0, 6, 0]]

    # I piece
    # x x x x
    i_piece = [[7, 7, 7, 7]]

    pieces = [o_piece, z_piece, s_piece, l_piece, j_piece, t_piece, i_piece]

	# queue of pieces to come
    num_next_pieces = 4
    next_pieces = []

    # position of the current piece that is falling down, relative to the top right corner of its matrix
    current_piece = None
    piece_row = 0
    piece_column = 0

    # size of the board
    width = 6
    height = 10

    # actual board matrix, from bottom to top, so row 0 is the bottom most row and row (height-1) is the topmost row
    board = []

    # views, to display and interact with the board (normally only one?)
    views = []


    #if fileName is set read initial board from the given filename
    #debug is a flag for additional debug print(statements)
    def __init__(self, width=10, height=20, turnTime=2, fileName=None, debug=False):

        self.debug = debug #debug flag
        self.height = height
        self.width = width
        self.turnTime = turnTime
        self.board = board = [[0 for j in range(self.width)] for i in range(self.height)]

        # read initial board from file
        if fileName != None:
            file = open(fileName, 'r')
            self.board = []
            line = file.readline()
            while line != "":
                self.height += 1
                row = []
                for c in list(line):
                    if c == '\n':
                        break
                    n = int(c)
                    if n < 0 or n > 7:
                        raise Error("Invalid character found in file ", fileName)
                    row.append(n)
                self.board.insert(0, row[:])
                line = file.readline()
            self.height = len(self.board)
            self.width = len(self.board[0])
            print("Board read from file", fileName, "with height", self.height, "and width", self.width)

        self.points = 0
        # fill in the next pieces queue initially
        self.current_piece = self.randomPiece()
        for i in range(self.num_next_pieces):
            self.next_pieces.append(self.randomPiece())
        self.nextPiece()

    def notify(self):
        for view in self.views:
            view.notify()

    def addView(self, view):
        self.views.append(view)

    def removeView(self, view):
        self.views.remove(view)

    def start(self):
        self.is_game_over = False
        #start the board thread that makes the current block fall
        thread1 = BoardThread(self)
        thread1.daemon = True
        thread1.start()

        # # make the piece fall, starting from the top middle
        # while not (self.is_game_over):
        #     user_in = raw_input()
        #     if user_in == 'l' or user_in == 'a':
        #         self.moveLeft()
        #     elif user_in == 'r' or user_in == 'd':
        #         self.moveRight()
        #     elif user_in == 'rot' or user_in == 's':
        #         self.rotate()
        #     self.notify()

    # Methods to be called from the views/controllers

    def moveRight(self):
        if self.isValidMove(self.current_piece, self.piece_row, self.piece_column + 1):
            self.piece_column += 1

    def moveLeft(self):
        if self.isValidMove(self.current_piece, self.piece_row, self.piece_column - 1):
            self.piece_column -= 1

    def moveDown(self):
        if self.canMoveDown():
            self.piece_row -= 1

    def cascadeDown(self):
        while self.canMoveDown():
            self.piece_row -= 1
        self.fixPiece()

    def rotate(self):
        if self.canRotate():
            print(self.piece_row, self.piece_column)
            self.current_piece = self.rotatePiece(self.current_piece)
            print(self.piece_row, self.piece_column)

    # Private methods
    def canMoveDown(self):
        return self.isValidMove(self.current_piece, self.piece_row - 1, self.piece_column)

    # IMPROVEMENT/BUG: be able to rotate the 7 (I piece) in this case
    # ~ ~ ~ ~ ~ ~
    # ~ ~ ~ ~ ~ ~
    # ~ ~ 7 7 7 7
    # ~ ~ ~ ~ ~ ~
    # ~ ~ 2 2 ~ ~
    # ~ ~ ~ 2 2 ~
    # 1 1 4 1 1 ~
    # 7 4 4 2 2 ~
    # 7 ~ 1 1 2 2
    # 7 ~ 1 1 ~ ~
    def canRotate(self):
        return self.isValidMove(self.rotatePiece(deepcopy(self.current_piece)), self.piece_row, self.piece_column)

    # TODO maybe should be a class method for a piece object...
    # rotate the piece by 90deg in clock orientation
    def rotatePiece(self, piece):
        piece_height = len(piece)
        piece_width = len(piece[0])
        rotated_piece = [[0 for i in range(piece_height)] for j in range(piece_width)]
        for i in range(piece_height):
            row = piece[i]
            for j in range(piece_width):
                rotated_piece[j][piece_height - i - 1] = piece[i][j]
        return rotated_piece

    def fixPiece(self):
        self.attachPiece()
        self.removeFilledRows()
        self.nextPiece()

    #attaches the currently falling piece to the board.
    def attachPiece(self):
        for i in range(len(self.current_piece)):
            row = self.current_piece[i]
            for j in range(len(row)):
                block = row[j]
                if block > 0:
                    if self.piece_row - i < self.height:  # needed so that the last piece gets added even if only partially
                        self.board[self.piece_row - i][self.piece_column + j] = block
                        if self.debug:
                            print(self.piece_row - i, ",", self.piece_column + j, "is now", block)

    def nextPiece(self):
        self.current_piece = self.next_pieces[0]
        self.piece_row = self.height - 1 + len(self.current_piece)
        self.piece_column = 0

        self.next_pieces = self.next_pieces[1:]
        self.next_pieces.append(self.randomPiece())

    def removeFilledRows(self):
        #check from the top so that we don't skip rows when they fall due to something dissapearing below
        for i in range(self.height-1,-1,-1):
            row = self.board[i]
            full = True
            for block in row:
                if block == 0:
                    full = False
                    break
            if full:
                if self.debug:
                    print("Removing row ", i , " " , row)
                self.points += 1
                self.board.remove(row)
                self.board.append([0 for j in range(self.width)])

    # Returns a random piece
    # Deepcopy is needed here since we might rotate this pieces and we don't want to rotate the original
    def randomPiece(self):
        n = random.randint(0, len(self.pieces) - 1)
        return deepcopy(self.pieces[n])

    # returns true if the piece can be in the specified position (height, column)
    # relative to its top right corner in the current orienation
    def isValidMove(self, piece, height, column):
        # left and right checks are trivial, just need to check the border of the piece against the borders of the board
        if column < 0:  # left side outside the left border of the board
            if self.debug:
                print("left bound")
            return False
        if column + len(piece[0]) - 1 >= self.width:  # right side outside the right border of the board
            if self.debug:
                print("right bound")
            return False

        # top check is not needed sine a piece can never go back up

        # check if it has reached the bottom row
        if height - (len(piece) - 1) < 0:
            if self.debug:
                print("bottom bound")
            return False

        # to check the piece against the current layout we need to check each block
        for i in range(len(piece)):
            row = piece[i]
            for j in range(len(row)):
                block = row[j]
                if block > 0:
                    if height - i < self.height:
                        if self.board[height - i][column + j] > 0:
                            if self.debug:
                                print("Overlap at row ", height - i, " and column ", column + j)
                            return False
        return True

    #replace if debug statements by something like this methood
    def printDebug(self, message):
        if self.debug:
            print(message)
