class ConsoleView():

    def __init__(self,board, input=True):
        self.board = board
        self.board.addView(self)
        self.board.start()
        if input:
            self.listenToInput()

    def listenToInput(self):
        while not (self.board.is_game_over):
            user_in = raw_input()
            if user_in == 'l' or user_in == 'a':
                self.board.moveLeft()
            elif user_in == 'r' or user_in == 'd':
                self.board.moveRight()
            elif user_in == 'rot' or user_in == 's':
                self.board.rotate()
            elif user_in == 'down' or user_in == 'w':
                self.board.cascadeDown()
            #update the view to include the move
            self.notify()


    def notify(self):
        self.print_board()

    def print_board(self):
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
