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
	print('RESET')
	return 'for the emperor'

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
	s = request.data.decode('ascii')
	fen = json.loads(s)
	board = chess.Board(fen['fen'])
	move = engine.get_move(board)
	print('move', move)
	board.push(move)
	move = str(move)
	
	return move