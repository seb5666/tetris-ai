class ConsoleView():

    def __init__(self,board):
        self.board = board

    def notify(self):
        print "Next pieces: TODO"
        print "Points:", self.board.points
        for i in range(self.board.height):
            if self.board.debug:
                print self.board.height - i - 1,
            for j in range(self.board.width):
                if self.board.height - i - 1 <= self.board.piece_row and \
                        self.board.height - i - 1 > self.board.piece_row - len(self.board.current_piece) and\
                        j >= self.board.piece_column and\
                        j < self.board.piece_column + len(self.board.current_piece[0]):
                    x = self.board.piece_row - (self.board.height - i - 1)
                    y = j - self.board.piece_column
                    if self.board.current_piece[x][y] > 0:
                        print self.board.current_piece[x][y],
                    else:
                        if (self.board.board[self.board.height - i - 1][j]) == 0:
                            print '~',
                        else:
                            print self.board.board[self.board.height - i - 1][j],
                else:
                    if (self.board.board[self.board.height - i - 1][j]) == 0:
                        print '~',
                    else:
                        print self.board.board[self.board.height - i - 1][j],
            print ""

        if self.board.debug:
            print " ",
            for j in range(self.board.width):
                print j,
            print ""
