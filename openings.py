import pickle
from chess import pgn
from chess.polyglot import zobrist_hash

dataset_file = open('fics_gm.pgn', encoding="utf-8")
dataset = []
ind = 1
MX_MOVE = 10

openings = dict()
results = set()

while True:
  #print(ind)
  game = pgn.read_game(dataset_file)
  #print(game.headers)
  if game is None:
    break
  results.add(game.headers['Result'])
  continue
  for i, move in enumerate(game.mainline_moves):
    if i >= MX_MOVE:
      break
    hc = zobrist_hash(board)
    board.push(move)
    hn = zobrist_hash(board)
    
    we = i % 2
    winner = game.headers

    x1, y1, x2, y2 = parse_move(move)

    if i % 2 == 1:
       x = np.flip(x, axis=[0, 1])
       x *= -1
       x1 = board_w - x1 - 1
       y1 = board_h - y1 - 1
       x2 = board_w - x2 - 1
       y2 = board_h - y2 - 1

    y = np.zeros((board_h, board_w, board_h, board_w), dtype='?')
    y[x1, y1, x2, y2] = 1
  #if 'WhiteElo'in game.headers and int(game.headers['WhiteElo']) >= THR:
  dataset.append(game)
  #if 'BlackElo'in game.headers and int(game.headers['BlackElo']) >= THR:
  #  dataset.append([-1, game])
  MX_MOVE 
  
   
  ind += 1
  if ind % 10000 == 0:
    print(ind, len(dataset))

print(results)
