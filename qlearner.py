from consoleView import ConsoleView
from board import Board
import random

class QLearner():

	def __init__(self, width=5, height=10):
		self.width = 5
		self.height = 10
		self.epsilon = 0.3 #probability of trying a random move
		self.alpha = 0.3 #learning rate
		self.gamma = 0.1 #discount factor
		self.actions = [i for i in range(4)] # [left, right, rotate, fall]

		self.train(trainingGames=1)

		self.board = Board(width=5, height=10)
		# TODO this gives weird output because the notify of the qlearer runs just after the other one, overlapping outputs to the standard output
		# self.consoleView =  ConsoleView(board, input=False)
		# self.board.addView(self.consoleView)
		self.board.addView(self)

		#initialise table storing the q function
		self.board.start()
		self.play()
	
	def play(self):
		while not self.board.is_game_over:
			pass
		print "GAME OVER"
			
	def notify(self):
		self.print_board()
		next_move = self.best_move(self.board)
		print "Moving: ", next_move
		self.move(self.board, next_move)

		#self.notify()
		# self.current_state()
		# self.print_board()

	def move(self, board, m):
		if m == 0:
			board.moveLeft()
		elif m == 1:
			board.moveRight()
		elif m == 2:
			board.rotate()
		elif m == 3:
			board.cascadeDown()

	def train(self, trainingGames=10):
		self.initialise_table()
		for i in range(trainingGames):
			trainingBoard = Board(width=self.width, height=self.height)
			trainingBoard.start()
			while not trainingBoard.is_game_over:
				next_move = self.training_move(trainingBoard)
				self.move(trainingBoard, next_move)
				#get reward
				#update q table at previous action...

	def best_move(self, board):
		state = self.state_in_board(board)
		temp = self.qTable
		for height in state:
			temp = temp[height]

		max = temp[0]
		max_index = 0
		for i in range(1, len(temp)):
			if temp[i] > max:
				max_index = i
		return max_index

	#use an epsilon greedy approach
	def training_move(self, board):
		if random.uniform(0.0,1.0) > self.epsilon:
			return self.best_move(board)
		else:
			return int(random.uniform(0.0,4.0))

	def initialise_table(self):
		#TODO only works for width 5!!!
		self.qTable = [[[[[[random.uniform(0.0,1.0) for i in range(len(self.actions))] for i in range(self.height)] for i in range(self.height)] for i in range(self.height)] for i in range(self.height)] for i in range(self.height)] 
		# print self.qTable
		print "Size: ", (self.height ** self.width) * 4 

	#returns the reward obtained by reaching the current state
	def reward_in_board(self, board):
		pass
	# Returns the current state of the board in our representation
	def state_in_board(self, board):
		state = [0 for j in range(board.width)]
		for j in range(board.width):
			for i in range(board.height):
				if board.board[i][j] > 0:
					state[j] = i
		return state

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
