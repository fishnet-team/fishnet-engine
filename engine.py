from opening_bot import OpeningMaster
import keras
import random
from keras.models import load_model

class Fishnet:
	def __init__(self, datafolder):
		#self.config = exec(open(datafolder + 'config.txt'))
		#self.net
		#self.net = load_model(datafolder + 'model.hdf5')
		self.opening = OpeningMaster(datafolder + 'opening-stats.dump')

	def get_move(self, board):
		if self.opening.has_info(board):
			return self.opening.get_move(board)
		moves = list(board.legal_moves)
		return moves[random.randint(0, len(moves) - 1)]