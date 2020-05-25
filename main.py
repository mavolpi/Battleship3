from random import randint

board = []

ship_number = int(raw_input("Number of Battleships: "))

print " "
print "You will have the same number of guesses as ships, plus a number of extras. "
print " "

double_length_ships = ship_number - 1

extra_guesses_allowed = int(raw_input("Number of Extra Guesses Allowed: "))
print " "

total_ships_alive = ship_number

ship_list = []

for x in range(0, 5):
  board.append(["O"] * 5)

def print_board(board):
  for row in board:
    print " ".join(row)

print_board(board)
print " "
print "Solution Key: "
print " "

def random_row(board):
  return randint(0, len(board) - 1)

def random_col(board):
  return randint(0, len(board[0]) - 1)

#Create 2-piece ships
def double_len_ship(ship_row, ship_col, ship_list):
  for i in range(double_length_ships):
    ship_list.append(ship_row + 1, ship_col + 1, 1)

def dup_ship_loc(ship_row, ship_col, ship_list):
  for i in range(len(ship_list)):
    if ship_list[i] == (ship_row, ship_col, 1):
      return True
  return False

while len(ship_list) < ship_number:
  ship_row = random_row(board)
  ship_col = random_col(board)
  if not dup_ship_loc(ship_row, ship_col, ship_list):
    ship_list.append((ship_row, ship_col, 1))
    if double_length_ships > 0:
      double_len_ship(ship_row, ship_col, ship_list)
      double_length_ships = double_length_ships - 1
    print (ship_row + 1, ship_col + 1)

print " "
  
#Guess checking Loop

for turn in range(extra_guesses_allowed + ship_number):
  
  if total_ships_alive == 0:
    print "You Win."
    break
 
  print "Turn", turn + 1
  guess_row = int(raw_input("Guess Row: ")) - 1
  guess_col = int(raw_input("Guess Col: ")) - 1

  if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
    print "Oops, that's not even in the ocean."
    print "Total Ships Alive %s" % total_ships_alive
    print " "
    continue

  elif(board[guess_row][guess_col] != "O"):
    print "You guessed that one already."
    print "Total Ships Alive %s" % total_ships_alive
    print " "
    continue

  for i,(ship_row, ship_col, life_status) in enumerate(ship_list):

    #print ship_list

    if guess_row == ship_row and guess_col == ship_col and life_status == 1:
      ship_list[i] = (ship_row, ship_col, 0)
      board[guess_row][guess_col] = "Z"

      total_ships_alive = total_ships_alive - 1

      print "Congratulations! You sunk a battleship!"
      print " "
      print "Total Ships Alive %s" % total_ships_alive
      print " "
      break

  if(board[guess_row][guess_col] == "O"):
    print "You missed my battleship!"
    print "Total Ships Alive %s" % total_ships_alive
    print " "
    board[guess_row][guess_col] = "X"

  if turn == (extra_guesses_allowed + ship_number-1):
    print "You are out of turns."
    print "Game Over."
    print " "
    break

  #print "Total Ships Alive %s" % total_ships_alive

  print_board(board)
  print " "