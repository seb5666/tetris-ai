from copy import deepcopy
from board import Board
from consoleView import ConsoleView
#from tkinterView import TkinterView

import sys


# O piece
# [
# 	[1,1],
# 	[1,1]
# ]

# uses assertions for now..
def testBoard():
    board = Board(fileName='test/board1')
    board.printBoard()
    print ""

    col = 4
    height = 8
    print "O piece at ", col, ",", height, " is True"
    assert board.isValidMove('o', height, col) == True

    col = 5
    height = 9
    print "O piece at ", col, ",", height, " is False"
    assert board.isValidMove('o', height, col) == False

    col = 2
    height = 9
    print "I piece at ", col, ",", height, " is True"
    assert board.isValidMove('i', height, col) == True

    col = 3
    height = 9
    print "I piece at ", col, ",", height, " is False"
    assert board.isValidMove('i', height, col) == False

    col = 1
    height = 5
    print "L piece at ", col, ",", height, " is False"
    assert board.isValidMove('l', height, col) == False


def testRotation():
    board = Board()
    for piece in board.pieces:
        p = deepcopy(piece)
        p1 = board.rotatePiece(p)
        p2 = board.rotatePiece(p1)
        p3 = board.rotatePiece(p2)
        p4 = board.rotatePiece(p3)
        for row in p1:
            for block in row:
                print block,
            print ""
        print ""
        assert p4 == p


def play():
    board = Board()
    view = ConsoleView(board)
    #view2 = TkinterView(board)
    board.addView(view)
    #board.addView(view2)
    board.start()


if (len(sys.argv) > 1):
    if sys.argv[1] == 'test':
        testRotation()
play()
