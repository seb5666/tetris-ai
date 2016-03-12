from copy import deepcopy
from board import Board
from consoleView import ConsoleView
#from tkinterView import TkinterView

import sys

# uses assertions for now..
# TODO test methods don't work anymore... Change to a proper testing framework and write some real unit tests...
def testBoard():
    board = Board(fileName='test/board1')
    board.printBoard()

#TODO write proper unit tests for the board class
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
                print(block),
            print("")
        print("")
        assert p4 == p


def play():
    board = Board(turnTime=1, width=6)
    game = ConsoleView(board)

def play_ai():
    game = QLearner()

#TODO write a proper command line interface...
if (len(sys.argv) > 1):
    if sys.argv[1] == 'test':
        testRotation()
#     if sys.argv[1] == 'qlearner':
#         play_ai()
else:        
    play()
