from __future__ import absolute_import, division, print_function
import copy
import random
import numpy as np

# 0: 'up', 1: 'left', 2: 'down', 3: 'right'
MOVES = [0, 1, 2, 3]
ACTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
MAXIMIZER = 1
CHANCEPLAYER = 0
BOARD_SIZE = 4
NO_DIRECTION = -1


class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.


	def __init__(self, root_state, depth_of_tree, current_score):
		self.initial_state = root_state
		self.depth = depth_of_tree
		self.starting_score = current_score


	# a high leven interface to return best decision to game
	def compute_decision(self):
		# build a simulator tree from the root node
		root = Simulator(copy.deepcopy(self.initial_state), self.starting_score, MAXIMIZER, NO_DIRECTION)
		# run expectimax from the root node
		root.buildTree(0, self.depth)
		# evaluate all the situations
		root.expectimax()
		# find the direction with max evaluation
		direction = -1
		maximum = -1
		for child in root.children:
			if maximum\
					< child.evaluation:
				direction = child.direction
				maximum = child.evaluation
		return direction


	# for comparison: randomly return a direction
	def trivial_decision(self):
		return random.randint(0, 3)


class Simulator:
	def __init__(self, state, utility, role, direction):
		self.tileMatrix = state
		self.total_points = utility
		self.children = []
		self.role = role  # 1 for max 0 for chance
		self.direction = direction
		self.evaluation = -1

	# recursively build the simulator tree on a root node
	def buildTree(self, level, height):
		# leaf node case, no child
		if level == height:
			return
		# if the node is a maximizer
		if self.role == MAXIMIZER:
			for direction in MOVES:
				child = Simulator(copy.deepcopy(self.tileMatrix), self.total_points, CHANCEPLAYER, direction)
				# if the move makes no difference, disregard it
				if not child.canMove(direction):
					continue
				# if the action makes a difference, perform the action and update the child's matrix and score
				else:
					# perform the action on the child
					child.move(direction)
					# recursively build the tree
					child.buildTree(level+1, height)
					# append the child to the parent's children list
					self.children.append(child)
		# if the node is a chance player
		elif self.role == CHANCEPLAYER:
			for i in range(0, BOARD_SIZE):
				for j in range(0, BOARD_SIZE):
					# find a blank tile
					if not self.tileMatrix[i][j]:
						child = Simulator(copy.deepcopy(self.tileMatrix), self.total_points, MAXIMIZER, NO_DIRECTION)
						# insert a 2 into the blank tile
						child.tileMatrix[i][j] = 2
						# recursively build the tree
						child.buildTree(level + 1, height)
						self.children.append(child)


	# evaluate each choice with a numerical value
	def expectimax(self):
		#for leaf nodes, simply return the score of its matrix
		if not len(self.children):
			self.evaluation = self.total_points
			return self.evaluation
		# if the current player is a maximizer:
		elif self.role == MAXIMIZER:
			# evaluate it by the highest score of its children's
			self.evaluation = max([c.expectimax() for c in self.children])

			return self.evaluation

		# if the current player is a chance player
		elif self.role == CHANCEPLAYER:
			# evaluate it by the mean score of its children's
			self.evaluation = float(sum([c.expectimax() for c in self.children])) / len(self.children)
			return self.evaluation


	# check if the max tile is on the corner
	def cornered (self):
		# if the largest number is on the corner, boost the score by 1.5
		max_tile = 0
		max_row = -1
		max_column = -1
		for i in range(0, BOARD_SIZE):
			for j in range(0, BOARD_SIZE):
				if self.tileMatrix[i][j] > max_tile:
					max_tile = self.tileMatrix[i][j]
					max_row = i
					max_column = j
				elif self.tileMatrix[i][j] == max_tile:
					# max tile can only be on the first or last row
					if i == 0 or i == 3:
						# if the largest tile is on the corners
						if j == 0 or j == 3:
							# update the cordinates
							max_row = i
							max_column = j
		if max_row == 0 or max_row == 3:
			if max_column == 0 or max_column == 3:
				return True
		return False


	# apply the direction to the board
	def move(self, direction):
		# perform the move
		self.moveTiles()
		self.mergeTiles()
		#self.placeRandomTile()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()


	# not sure what it does
	def rotateMatrixClockwise(self):
		tm = self.tileMatrix
		for i in range(0, int(BOARD_SIZE/2)):
			for k in range(i, BOARD_SIZE - i - 1):
				temp1 = tm[i][k]
				temp2 = tm[BOARD_SIZE - 1 - k][i]
				temp3 = tm[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
				temp4 = tm[k][BOARD_SIZE - 1 - i]
				tm[BOARD_SIZE - 1 - k][i] = temp1
				tm[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
				tm[k][BOARD_SIZE - 1 - i] = temp3
				tm[i][k] = temp4


	def moveTiles(self):
		tm = self.tileMatrix
		for i in range(0, BOARD_SIZE):
			for j in range(0, BOARD_SIZE - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, BOARD_SIZE - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][BOARD_SIZE - 1] = 0


	def mergeTiles(self):
		tm = self.tileMatrix
		for i in range(0, BOARD_SIZE):
			for k in range(0, BOARD_SIZE - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.total_points += tm[i][k]
					self.moveTiles()


	# check if the game can contitnue
	def checkIfCanGo(self):
		tm = self.tileMatrix
		for i in range(0, BOARD_SIZE ** 2):
			if tm[int(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
				return True
		for i in range(0, BOARD_SIZE):
			for j in range(0, BOARD_SIZE - 1):
				if tm[i][j] == tm[i][j + 1]:
					return True
				elif tm[j][i] == tm[j + 1][i]:
					return True
		return False


	# check if the direction makes a difference
	def canMove(self, direction):
		# always rotate the matrix to a fix direction
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		# check if the rotated matrix can move in the direction
		tm = self.tileMatrix
		for i in range(0, BOARD_SIZE):
			for j in range(1, BOARD_SIZE):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False
