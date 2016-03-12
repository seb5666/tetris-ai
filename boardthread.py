import threading
import time

# thread responsible for making the current block fall at regular intervals, the time is defined in the board as board.turnTime
class BoardThread(threading.Thread):
    def __init__(self, board):
        super(BoardThread, self).__init__()
        self.board = board

    def run(self):
        self.board.notify()
        while not self.board.is_game_over:
            #wait the given amount of time
            time.sleep(self.board.turnTime)
            #notify the views to update the board
            self.board.notify() 
            self.board.moveDown()

        print("Game over, press enter to exit")
        self.board.is_game_over = True
