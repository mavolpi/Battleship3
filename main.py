from random import randint

board = []

print("Configure your fleet:")
try:
    ships_1 = int(input("Number of 1-piece ships: "))
    ships_2 = int(input("Number of 2-piece ships: "))
    ships_3 = int(input("Number of 3-piece ships: "))
except ValueError:
    print("Please enter valid numbers only.")
    exit(1)

total_ships = ships_1 + ships_2 + ships_3
total_ship_segments = ships_1 + (ships_2 * 2) + (ships_3 * 3)

print(" ")
print("You will have the same number of guesses as ship segments, plus a number of extras. ")
print("Total ship segments: %d" % total_ship_segments)
print(" ")

try:
    extra_guesses_allowed = int(input("Number of Extra Guesses Allowed: "))
except ValueError:
    print("Please enter valid numbers only.")
    exit(1)
print(" ")

total_ships_alive = total_ships
total_segments_alive = total_ship_segments

ship_list = []

for x in range(0, 5):
  board.append(["O"] * 5)

def print_board(board):
  for row in board:
    print(" ".join(row))

print_board(board)
print(" ")
print("Solution Key: ")
print(" ")

def random_row(board):
  return randint(0, len(board) - 1)

def random_col(board):
  return randint(0, len(board[0]) - 1)

def can_place_ship(start_row, start_col, length, orientation, board):
  if orientation == 'horizontal':
    if start_col + length > 5:
      return False
    for i in range(length):
      if board[start_row][start_col + i] != "O":
        return False
  else:  # vertical
    if start_row + length > 5:
      return False
    for i in range(length):
      if board[start_row + i][start_col] != "O":
        return False
  return True

def place_ship_on_board(start_row, start_col, length, orientation, board, ship_id):
  segments = []
  if orientation == 'horizontal':
    for i in range(length):
      board[start_row][start_col + i] = str(ship_id)
      segments.append((start_row, start_col + i))
  else:  # vertical
    for i in range(length):
      board[start_row + i][start_col] = str(ship_id)
      segments.append((start_row + i, start_col))
  return segments

temp_board = []
for x in range(0, 5):
  temp_board.append(["O"] * 5)

ship_id = 1

for i in range(ships_1):
  placed = False
  attempts = 0
  while not placed and attempts < 100:
    ship_row = random_row(board)
    ship_col = random_col(board)
    if can_place_ship(ship_row, ship_col, 1, 'horizontal', temp_board):
      segments = place_ship_on_board(ship_row, ship_col, 1, 'horizontal', temp_board, ship_id)
      ship_list.append({'id': ship_id, 'length': 1, 'segments': segments, 'hits': 0})
      print("1-piece ship at:", [(r+1, c+1) for r, c in segments])
      ship_id += 1
      placed = True
    attempts += 1
  if not placed:
    print("Warning: Could not place 1-piece ship #%d after 100 attempts" % (i+1))

for i in range(ships_2):
  placed = False
  attempts = 0
  while not placed and attempts < 100:
    ship_row = random_row(board)
    ship_col = random_col(board)
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
    if can_place_ship(ship_row, ship_col, 2, orientation, temp_board):
      segments = place_ship_on_board(ship_row, ship_col, 2, orientation, temp_board, ship_id)
      ship_list.append({'id': ship_id, 'length': 2, 'segments': segments, 'hits': 0})
      print("2-piece ship at:", [(r+1, c+1) for r, c in segments])
      ship_id += 1
      placed = True
    attempts += 1
  if not placed:
    print("Warning: Could not place 2-piece ship #%d after 100 attempts" % (i+1))

for i in range(ships_3):
  placed = False
  attempts = 0
  while not placed and attempts < 100:
    ship_row = random_row(board)
    ship_col = random_col(board)
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
    if can_place_ship(ship_row, ship_col, 3, orientation, temp_board):
      segments = place_ship_on_board(ship_row, ship_col, 3, orientation, temp_board, ship_id)
      ship_list.append({'id': ship_id, 'length': 3, 'segments': segments, 'hits': 0})
      print("3-piece ship at:", [(r+1, c+1) for r, c in segments])
      ship_id += 1
      placed = True
    attempts += 1
  if not placed:
    print("Warning: Could not place 3-piece ship #%d after 100 attempts" % (i+1))

print(" ")
  
#Guess checking Loop

for turn in range(extra_guesses_allowed + total_ship_segments):
  
  if total_ships_alive == 0:
    print("You Win.")
    break
 
  print("Turn", turn + 1)
  try:
    guess_row = int(input("Guess Row: ")) - 1
    guess_col = int(input("Guess Col: ")) - 1
  except ValueError:
    print("Please enter valid numbers only.")
    continue

  if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
    print("Oops, that's not even in the ocean.")
    print("Total Ships Alive %s" % total_ships_alive)
    print(" ")
    continue

  elif(board[guess_row][guess_col] != "O"):
    print("You guessed that one already.")
    print("Total Ships Alive %s" % total_ships_alive)
    print(" ")
    continue

  hit_ship = False
  for ship in ship_list:
    if (guess_row, guess_col) in ship['segments']:
      board[guess_row][guess_col] = "Z"
      ship['hits'] += 1
      total_segments_alive -= 1
      
      if ship['hits'] == ship['length']:
        total_ships_alive -= 1
        print("Congratulations! You sunk a %d-piece battleship!" % ship['length'])
      else:
        print("Hit! You damaged a %d-piece battleship!" % ship['length'])
      
      print(" ")
      print("Total Ships Alive: %s" % total_ships_alive)
      print("Total Segments Remaining: %s" % total_segments_alive)
      print(" ")
      hit_ship = True
      break

  if not hit_ship and board[guess_row][guess_col] == "O":
    print("You missed my battleship!")
    print("Total Ships Alive: %s" % total_ships_alive)
    print("Total Segments Remaining: %s" % total_segments_alive)
    print(" ")
    board[guess_row][guess_col] = "X"

  if turn == (extra_guesses_allowed + total_ship_segments-1):
    print("You are out of turns.")
    print("Game Over.")
    print(" ")
    break


  print_board(board)
  print(" ")
