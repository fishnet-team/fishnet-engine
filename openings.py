import pickle
from chess import pgn
from chess.polyglot import zobrist_hash

dataset_file = open('fics_gm.pgn', encoding="utf-8")
ind = 1
MX_MOVE = 10

openings = dict()

text2res = {'1-0': 1, '0-1': -1, '1/2-1/2':0}

while True:
  #print(ind)
  game = pgn.read_game(dataset_file)
  #print(game.headers)
  if game is None:
    break
  if 'Result' not in game.headers or game.headers['Result'] not in text2res:
    continue
  curr_res = text2res[game.headers['Result']]

  for i, move in enumerate(game.mainline_moves):
    if i >= MX_MOVE:
      break
    hc = zobrist_hash(board)
    board.push(move)
    hn = zobrist_hash(board)

    if hc not in openings:
      openings[hc] = dict()
    if hn not in openings[hc]:
      openings[hc][hn] = [0, 0, 0]
    openings[hc][hn][curr_res] += 1
    curr_res *= -1
  ind += 1

pickle.dump(openings, open("openings-stats.dump", "wb"))