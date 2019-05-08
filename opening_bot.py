from chess import pgn
from chess.polyglot import zobrist_hash
import chess.polyglot

class OpeningMaster:
	def __init__(self, stat_filename, thr=5, tempature=1):
		self.stat = chess.polyglot.MemoryMappedReader(stat_filename)

		'''with chess.polyglot.open_reader(stat_filename) as reader:
		    for entry in reader.find_all(board):
		    	print(entry.move, entry.weight, entry.learn, entry.key)
		    	if entry.key not in self.stat:
		    		self.stat[entry.key] = []
		    	else:
		    		self.stat[entry.key].append([entry.weight, entry.move])'''
		self.thr = thr
		self.tempature = tempature

	#def has_info(self, board):
	#	hc = zobrist_hash(board)
	#	return hc in self.stat

	def get_move(self, board):
		return self.stat.get(board)