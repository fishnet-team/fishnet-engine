from opening_bot import OpeningMaster
import keras
import random
from keras.models import load_model
import os
from copy import copy
import itertools
from keras.utils import to_categorical
import chess

import numpy as np
import pandas as pd

class Fishnet:
	def __init__(self, datafolder, MX_BRANCHING=10, MX_GAN_DEPTH=2):
		self.net = load_model(datafolder + 'model.hdf5')
		self.net._make_predict_function()
		print(self.net.summary())
		
		self.opening = OpeningMaster(datafolder + 'varied.bin')
		
		self.MX_BRANCHING = MX_BRANCHING
		self.MX_GAN_DEPTH = MX_GAN_DEPTH
		self.board_w = 8
		self.board_h = 8
		self.INF = 1791791791
		self.cost = {'p': 1, 'k': self.INF, 'q': 9, 'r': 5, 'b': 3, 'n': 3}

		self.figures = ["r", "n", "b", "q", "k", "p"]
		self.vec_by_figure = {}

		for i, fig in enumerate(self.figures):
		    self.vec_by_figure[fig] = to_categorical(i, num_classes=len(self.figures))

	def score_function(self, board):
		if board.is_game_over():
			res = board.result()
			if res == '1-0':
				return self.INF
			elif res == '0-1':
				return -self.INF
			else:
				return 0
		balance = 0
		for el in board.fen().split()[0]:
			if el.lower() in self.figures:
				balance += self.cost[el.lower()] * (1 - 2 * (el != el.lower()))
		return balance

	
	def guaranteed_balance(self, board, depth_left):
		if depth_left == 0:
			return self.score_function(board)
		best = None
		for move in board.legal_moves:
			temp = board.copy()
			temp.push(move)
			balance = self.guaranteed_balance(temp, depth_left - 1)
			if balance is None:
				continue
			if best is None:
				best = balance
			elif board.turn and balance > best:
				best = balance
			elif not board.turn and balance < best:
				best = balance
		return best

	def chess_to_np(self, board):
		ret = []
	    
		for line in reversed(str(board).split("\n")):
		    for fig in line.split():
		        if fig == ".":
		            ret.append(np.array([0] * len(self.figures)))
		        elif fig.islower():
		            ret.append(self.vec_by_figure[fig] * -1)
		        else:
		            ret.append(self.vec_by_figure[fig.lower()])
		res = np.array(ret).reshape(1, self.board_h, self.board_w, len(self.figures))
		if not board.turn:
			res = np.flip(res, axis=[1, 2])
			res *= -1
		return res

	def moveid2move_cords(self, mid):
		x1 = mid // 8 ** 3
		mid %= 8 ** 3
		y1 = mid // 8 ** 2
		mid %= 8 ** 2
		x2 = mid // 8
		mid %= 8
		y2 = mid
		return (x1, y1, x2, y2)

	def movec2move(self, mid):
		(x1, y1, x2, y2) = mid
		return chr(x1 + ord('a')) + str(y1 + 1) + chr(x2 + ord('a')) + str(y2 + 1)

	def reverse_move(self, move):
		return (7 - move[i] for i in range(len(move)))

	def get_neural_move_rating(self, board):
		data = self.chess_to_np(board)
		res = list(self.net.predict(data)[0])
		correct_moves = []
		for i in range(len(res)):
			move = self.moveid2move_cords(i)
			if not board.turn:
				move = self.reverse_move(move)
			move = self.movec2move(move)
			if chess.Move.from_uci(move) in board.legal_moves:
				correct_moves.append((res[i], chess.Move.from_uci(move)))
		correct_moves.sort(reverse=True)
		return correct_moves

	def guided_search(self, board, depth_left=4):
		if depth_left == 0:
			return self.score_function(board)
		best = None

		for move in self.get_neural_move_rating(board)[:self.MX_BRANCHING]:
			temp = board.copy()
			temp.push(move[1])
			balance = self.guaranteed_balance(temp, depth_left - 1)
			if balance is None:
				continue
			if best is None:
				best = balance
			elif board.turn and balance > best:
				best = balance
			elif not board.turn and balance < best:
				best = balance
		return best

	def neural_play(self, board):
		print('NEURAL MAGIC')
		correct_moves = self.get_neural_move_rating(board)[:self.MX_BRANCHING]
		scored_moves = []
		for el in correct_moves:
			temp = board.copy()
			temp.push(el[1])
			scored_moves.append((self.guided_search(temp, self.MX_GAN_DEPTH), 
								el[0], el[1]))
		scored_moves.sort(reverse=True)
		return scored_moves[0][-1]

	def get_move(self, board):
		move = self.opening.get_move(board)
		if move is not None:
			move = move.move()
		else:
			move = self.neural_play(board)
		temp = board.copy()
		temp.push(move)
		print('move:', move, 'score:', self.score_function(temp))
		return move