from flask import Flask
from engine import Fishnet
from flask import send_file
from flask import request
import chess
import json

app = Flask(__name__)

engine = Fishnet('fishnet-data/')
board = chess.Board()

@app.route('/reset')
def reset_board():
	board.reset()
	return 'for the emperor'

'''@app.route('/move/{}')
def add_move(move):
	print('got move: ' + move)
	board.push(move)
	return 'done'
'''

@app.route('/')
def index():
	return send_file('index.html')

@app.route('/js/<data>')
def js_chessboard(data):
	print('js_chessboard: ', data)
	return send_file('js/' + data)

@app.route('/img/chesspieces/wikipedia/<data>')
def send_img(data):
	return send_file('img/chesspieces/wikipedia/' + data)

@app.route('/css/<data>')
def css_chessboard(data):
	return send_file('css/' + data)

@app.route('/get_move', methods=['POST'])
def get_move():
	#print(request.args)
	#print(request.data)
	#print(request.data.decode('ascii'))
	s = request.data.decode('ascii')
	#print(s, type(s))
	fen = json.loads(s)
	#print(fen)
	board = chess.Board(fen['fen'])
	move = engine.get_move(board)
	print('move', move)
	board.push(move)
	move = str(move)
	#move = move[:2] + '-' + move[2:]
	
	return move