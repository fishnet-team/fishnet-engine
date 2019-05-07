import pickle
from chess import pgn
from chess.polyglot import zobrist_hash


class OpeningMaster:
	def __init__(self, stat_filename, thr=5, tempature=1):
		self.stat = pickle.load(open(stat_filename, 'rb'))
		self.thr = thr
		self.tempature = tempature

	def has_info(self, board):
		hc = zobrist_hash(board)
		if hc not in self.stat:
			return False
		cnt = 0
		for el in self.stat[hc]:
			cnt += sum(self.stat[hc][el])
		return cnt >= self.thr

	def get_move(self, board):
		moves = []
		hc = zobrist_hash(board)
		for el in self.stat[hc]:
			#print(hc, self.stat[hc])
			if sum(self.stat[hc][el]) < self.thr:
				continue
			moves.append([(self.stat[hc][el][1] - self.stat[hc][el][-1]) 
						/ sum(self.stat[hc][el]) / self.tempature, el])
		moves.sort()

		choice = 0
		need = moves[choice][-1]

		for move in board.legal_moves:
			board.push(move)
			if zobrist_hash(board) == need:
				return move
			board.pop()