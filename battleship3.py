from player import Player
from board import Board
import os

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
MISS = '.'
HIT = '*'
SUNK = '#'	


def ascii_art():
	ascii_art = '''
______       _   _   _           _     _       
| ___ \     | | | | | |         | |   (_)      
| |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __  
| ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
| |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) |
\____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|    
'''
	return ascii_art

def prompt_location(player, ship_type, ship_size):
	if ship_type == None:
		location = input("\n{}, select your target: ".format(player))
	else:
		location = input("\n{}, select location of the {} ({} spaces): ".format(player, ship_type, ship_size))
	if is_loc_valid(location):
		return location
	else:
		print("Error! Must have letters A - J and numbers 1 - 10. For example: G7")
		return prompt_location(player, ship_type, ship_size)


def is_loc_valid(location):
	valid_letters = "abcdefghij"
	valid_numbers = "123456789"
	if len(location) == 3:
		if location[0].lower() in valid_letters and location[1:] == "10":
			return True
	elif len(location) == 2:
		if location[0].lower() in valid_letters and location[1] in valid_numbers:
			return True
	else:
		return False
	

def prompt_orientation():
	orientation = input("Is the ship horizontal(h) or vertical(v)? ")
	if orientation.lower() == "v" or orientation.lower() == "h":
		return orientation
	else:
		print("Error! Please enter 'h' for horizontal or 'v' for vertical.")
		return prompt_orientation()


def is_orientation_valid(orientation, location, ship_size):
	if orientation.lower() == "h":
		if ord(location[0].lower()) + ship_size <= ord("k"):
			return True
		else:
			return False
	else:
		if int(location[1:]) - 1 + ship_size <= 10:
			return True
		else:
			return False

def convert_locs(location):
	'''converts input location to a tuple of board
	coordinates'''
	row_ind = ord(location[0].lower()) - ord("a")
	col_ind = int(location[1:]) - 1
	return row_ind, col_ind


def get_ship_locs(location, orientation, ship_size):
	'''Returns a tuple of all the coordinates the ship
	occupies in the board'''
	ship_locs = []
	#row_ind, col_ind = convert_locs(location)
	row_ind = ord(location[0].lower()) - ord("a")
	col_ind = int(location[1:]) - 1
	index = 0
	if orientation == "h":
		for i in range(ship_size):
			ship_locs.append((row_ind + index, col_ind))
			index += 1
	else:
		for i in range(ship_size):
			ship_locs.append((row_ind, col_ind + index))
			index += 1
	return ship_locs


def ship_overlap(ship_locs, ships):
	for item in ship_locs:
		for item2 in ships:
			if item in item2.positions:
				return True


def update_board(player, ship_locs, orientation):
	for loc in ship_locs:
		if orientation == "h":
			player.board.board[loc[1]][loc[0]] = HORIZONTAL_SHIP
		else:
			player.board.board[loc[1]][loc[0]] = VERTICAL_SHIP
			

def place_ships(player, ships):
	clear()
	player.board.print_board()
	location = prompt_location(player.name, ships.ship_type, ships.size)
	orientation = prompt_orientation().lower()

	if not is_orientation_valid(orientation, location, ships.size):
		print("Error! Ship does not fit the board. Enter another location or orientation.")
		input("Press enter to continue.")
		place_ships(player, ships)
	else:
		ship_locs = get_ship_locs(location, orientation, ships.size)
	
		if ship_overlap(ship_locs, player.ships):
			print("Error! Ship overlaps with previously placed ship. Choose another location.")
			input("Press enter to continue.")
			place_ships(player, ships)
		else:
			ships.positions.extend(ship_locs)
			update_board(player, ship_locs, orientation)


def clear():
	#clears screen whenever called
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def is_ship_hit(player, ships, shot_loc):
	'''checks if shot hits opponent's ship. Returns
	which type of ship was hit'''
	for ship in ships:
		if shot_loc in ship.positions:
			#print("You HIT {}'s {}".format(player.opponent.name, ship.ship_type))
			return ship

def update_game_board(player, coord, char):
	'''updates player's current game board'''
	player.gameboard.board[coord[0]][coord[1]] = char


def is_ship_sunk(ship_hit):
	if ship_hit.health == 0:
		return ship_hit.positions

def winner(sunk_ships):
	if sunk_ships == 5:
		return True


def game():
	print(ascii_art())
	print("Player 1")
	Player1 = Player()
	print("Player 2")
	Player2 = Player()

	Player1.opponent = Player2
	Player2.opponent = Player1
	players = (Player1, Player2)

	
	
	#asks players to place their ships
	input("Players, enter location of your ships. Press enter to continue.")
	clear()
	for player in players:
		#player.board.print_board()
		for ships in player.ships:
			place_ships(player, ships)
			clear()
			player.board.print_board()
		input("You have placed all your ships. Press enter to continue.")
	
	#battle commences
	clear()
	input("Let the battles commence! Press enter to continue")
	clear()
	
	for player in players:
		player.gameboard.print_board()
		
		shot_loc = prompt_location(player.name, None, None)
		shot_loc = convert_locs(shot_loc)
		print(shot_loc) #
		player.shots_location.append((1,1)) #

		while shot_loc in player.shots_location:
			clear()
			print("You already fired in this location. Try another one")
			player.gameboard.print_board()
			shot_loc = prompt_location(player.name, None, None)
			shot_loc = convert_locs(shot_loc)
		#if is_hit(shot_loc, opponent.ship.positions):
		#for ship in player.opponent.ships:
		if is_ship_hit(player, player.opponent.ships, shot_loc): #shot_loc in ship.positions:
			clear()
			ship_hit = is_ship_hit(player, player.opponent.ships, shot_loc)
			print("You HIT {}'s {}".format(player.opponent.name, ship_hit.ship_type))
			ship_hit.health -= 1
			player.shots_location.append(shot_loc)
			if is_ship_sunk(ship_hit):
				player.sunk += 1
				print("Excellent shot {}'s {} is now SUNKED!".format(player.opponent.name, ship_hit.ship_type))
				sunk_coords = is_ship_sunk(ship_hit)
				for coords in sunk_coords:
					update_game_board(player, coords, SUNK)
				player.gameboard.print_board()
				
				if winner(player.sunk):
					clear()
					break
						
						
			else:
			# ship hit but not sunked yet
				update_game_board(player, shot_loc, HIT)
				player.gameboard.print_board()
				input("Press enter to continue")
				clear()
			
		else:
			print("You missed! Try again.")
			update_game_board(player, shot_loc, MISS)
			player.gameboard.print_board()

	print("Congratulations! You have demolished {}'s entire fleet.".format(player.opponent.name))
	print("{}, you are the WINNER!".format(player.name))
	input("Press enter to see both player boards.")
	# display boards
	print("\n {}'s board: \n".format(Player1.name))
	Player1.board.print_board()
	print("\n {}'s board: \n".format(Player2.name))
	Player1.board.print_board()

	input("Press enter to quit the game. Thanks for playing.")




if __name__ == "__main__":
	game()