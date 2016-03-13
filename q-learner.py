from board import Board
from copy import deepcopy
import random
import math
trim_limit = 3

b = Board(height=10, width=5)

b.start()
number_of_board_states = 7 ** b.width

piece_array = []
# Calculate the rotation map
for piece in b.pieces:
    for i in range(4):
        piece = deepcopy(piece)
        if piece not in piece_array:
            piece_array.append(piece)
        piece = b.rotatePiece(deepcopy(piece))
available_actions = [ 'w', 'a', 's', 'd' ]

class QLearner:
    points_at_last_check = 0
    death_punishment = -5.0
    inactivity_punishment = -1.0
    learning_rate = 1.0
    discount_factor = 0.99
    q_values = [[[[0 for action in range(len(available_actions))] for column in range(b.width)] for piece_type in range(len(piece_array))] for board_state in range(number_of_board_states)]

    def encode_board(self, board):
        total = 0
        multiplier = 1
        heights = self.get_heights(board)
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
    def get_heights(self, board):
        heights = [0 for j in range(len(board[0]))]
        for j in range(len(board[0])):
            for i in range(len(board) - 1, -1, -1):
                if board[i][j] > 0:
                    heights[j] = i + 1
                    break
        return heights

    def get_piece_type(self, board):
        return piece_array.index(board.current_piece)

    def get_point_difference(self, board):
        difference = board.points - self.points_at_last_check
        self.points_at_last_check = board.points
        return difference

    def decide_action(self, board):
        board_state = self.encode_board(board.board)
        piece_type = self.get_piece_type(board)
        piece_column = board.piece_column

        action_rewards = self.q_values[board_state][piece_type][piece_column]

        exp_action_rewards = [math.exp(reward) for reward in action_rewards]
        cumulative_sum = self.get_cumulative_sum(exp_action_rewards)

        random_num = random.random() * cumulative_sum[-1]
        action_index = 0
        while True:
            if action_index == len(exp_action_rewards) - 1:
                break
            elif random_num > cumulative_sum[action_index]:
                action_index += 1
            else:
                break

        action = available_actions[action_index]

        self.perform_action(board, action)
        reward = self.get_point_difference(board)

        if board.is_game_over:
            reward = self.death_punishment
            board.start()

        new_board_state = self.encode_board(board.board)
        new_piece_type = self.get_piece_type(board)
        new_piece_column = board.piece_column

        if new_board_state == board_state and new_piece_type == piece_type and new_piece_column == piece_column:
            reward = self.inactivity_punishment

        optimal_future_value = max(self.q_values[new_board_state][new_piece_type][new_piece_column])
        old_q_value = self.q_values[board_state][piece_type][piece_column][action_index]
        learned_value = reward + self.discount_factor * optimal_future_value
        self.q_values[board_state][piece_type][piece_column][action_index] = old_q_value + self.learning_rate * (learned_value - old_q_value)

    def get_cumulative_sum(self, list_to_sum):
        cumulative_list = [ ]
        for i, x in enumerate(list_to_sum):
            cumulative_list.append(x if i == 0 else cumulative_list[i - 1] + x)
        return cumulative_list

    def play_optimally(self, board):
        board_state = self.encode_board(board.board)
        piece_type = self.get_piece_type(board)
        piece_column = board.piece_column
        action_rewards = self.q_values[board_state][piece_type][piece_column]
        action_index = self.arg_max(action_rewards)
        action = available_actions[action_index]

        for row in board.board:
            print(row)
        print(action_rewards)
        print(board.current_piece)
        print(piece_column)

        self.perform_action(board, action)
        if board.is_game_over:
            board.start()

        new_board_state = self.encode_board(board.board)
        new_piece_type = self.get_piece_type(board)
        new_piece_column = board.piece_column
        if new_board_state == board_state and new_piece_type == piece_type and new_piece_column == piece_column:
            print("Inactive")

    def perform_action(self, board, action):
        if action == 'a':
            board.moveLeft()
        elif action == 'd':
            board.moveRight()
        elif action == 's':
            board.rotate()
        elif action == 'w':
            board.cascadeDown()

    def arg_max(self, ar):
        max_index = 0
        max_value = ar[0]
        for index, value in enumerate(ar):
            if value > max_value:
                max_index = index
                max_value = value
        return max_index

q_learner = QLearner()
last_point_increase_time = 0
last_point = 0
last_death_time = 0
for x in range(10000000):
    q_learner.decide_action(b)
    if b.points != last_point:
        print(last_point_increase_time)
        last_point_increase_time = 0
        last_point = b.points
    last_point_increase_time += 1
    if x % 10000 == 0:
        print("At", x)
        print("Number of deaths", b.number_of_deaths)
        b.number_of_deaths = 0
    if x % 1000000 == 0:
        print("At", x)
        for y in range(10000):
            q_learner.decide_action(b)
            for i in range(len(b.board) - 1, 0, -1):
                print(b.board[i])
            print()
            print()
            if b.points != last_point:
                print(last_point_increase_time)
                last_point_increase_time = 0
                last_point = b.points
            last_point_increase_time += 1
        print("Fin ", x)
