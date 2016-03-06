import threading
import time

# thread responsible for making the current block fall at regular intervals, the time is defined in the board as board.turnTime
class BoardThread(threading.Thread):
    def __init__(self, board):
        super(BoardThread, self).__init__()
        self.board = board

    def run(self):
        self.board.notify()
        while True:
            #wait the given amount of time
            time.sleep(self.board.turnTime)
            #notify the views to update the board
            self.board.notify() 
            if self.board.canMoveDown():
                self.board.piece_row -= 1
            else:
                if self.board.debug:
                    print("reached bottom")
                
                #check if game is over
                if self.board.piece_row >= self.board.height:
                    break

                # fix piece to the board
                self.board.fixPiece()

        print "Game over, press enter to exit"
        self.board.is_game_over = True