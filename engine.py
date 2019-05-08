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

'''

dataset_x = []
dataset_y = []

for game_idx in itertools.count():
    game = pgn.read_game(dataset_file)

    if game is None:
        break

    board = game.board()

    for i, move in enumerate(game.mainline_moves()):
        x = chess_to_np(board)

    x1, y1, x2, y2 = parse_move(move)

    if i % 2 == 1:
        x = np.flip(x, axis=[0, 1])

        x1 = board_w - x1 - 1
        y1 = board_h - y1 - 1
        x2 = board_w - x2 - 1
        y2 = board_h - y2 - 1

    y = np.zeros((board_h, board_w, board_h, board_w))
    y[x1, y1, x2, y2] = 1

    dataset_x.append(x)
    dataset_y.append(y)

'''

class Fishnet:
	def __init__(self, datafolder):
		self.net = load_model(datafolder + 'model.hdf5')
		self.net._make_predict_function()
		print(self.net.summary())
		self.opening = OpeningMaster(datafolder + 'varied.bin')

		self.board_w = 8
		self.board_h = 8

		self.figures = ["r", "n", "b", "q", "k", "p"]
		self.vec_by_figure = {}

		for i, fig in enumerate(self.figures):
		    self.vec_by_figure[fig] = to_categorical(i, num_classes=len(self.figures))

	#def score_function(self, board):
	#	# always for white
	#	if board.

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

	def neural_play(self, board):
		print('NEURAL MAGIC')
		data = self.chess_to_np(board)
		#print(data)
		#print(data.shape)
		res = list(self.net.predict(data)[0])
		correct_moves = []
		for i in range(len(res)):
			move = self.moveid2move_cords(i)
			#print(i, move)
			if not board.turn:
				move = self.reverse_move(move)
			move = self.movec2move(move)
			#print(move)#, chess.Move.from_uci(move), list(board.legal_moves))
			if chess.Move.from_uci(move) in board.legal_moves:
				correct_moves.append((res[i], chess.Move.from_uci(move)))
		correct_moves.sort(reverse=True)
		#print(correct_moves)
		return correct_moves[0][1]

	def get_move(self, board):
		move = self.opening.get_move(board)
		if move is not None:
			move = move.move()
			return move
		return self.neural_play(board)