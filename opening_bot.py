from chess import pgn
from chess.polyglot import zobrist_hash
import chess.polyglot

class OpeningMaster:
	def __init__(self, stat_filename):
		self.stat = chess.polyglot.MemoryMappedReader(stat_filename)

	def get_move(self, board):
		return self.stat.get(board)