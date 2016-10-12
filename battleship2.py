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
		location = input("\n{}, select your target ".format(player))
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

def ship_hit(player, shot_loc, ships, char):
	'''checks if shot hits opponent's ship. Updates board
	and print message of the hit and the ship'''
	for ship in ships:
		if shot_loc in ship.positions:
			update_game_board(player, shot_loc, char)
			player.gameboard.print_board()
			print("You HIT {}'s {}".format(player.opponent.name, ship.ship_type))
			return ship.health - 1

def update_game_board(player, coord, char):
	'''updates player's current game board'''
	player.gameboard.board[coord[0]][coord[1]] = char


def game():
	print(ascii_art())
	print("Player 1")
	Player1 = Player()
	print("Player 2")
	Player2 = Player()

	Player1.opponent = Player2
	Player2.opponent = Player1
	players = (Player1, Player2)

	print(Player1.opponent.name)
	print(Player1.opponent.ships) #
	#asks players to place their ships
	input("Players, enter location of your ships. Press enter to continue.")
	clear()
	for player in players:
		#player.board.print_board()
		for ships in player.ships:
			print(player.opponent.ships) #
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
		print(player.opponent.name)
		shot_loc = prompt_location(player.name, None, None)
		shot_loc = convert_locs(shot_loc)
		print(shot_loc) #
		player.shots_location.append((1,1)) #
		while shot_loc in player.shots.location:
			print("You already fired in this location. Try another one")
			shot_loc = prompt_location(player.name, None, None)
			shot_loc = convert_locs(shot_loc)
		#if is_hit(shot_loc, opponent.ship.positions):
		#for ship in player.opponent.ships:
		if not ship_hit(player, shot_loc, player.opponent.ships, HIT): #shot_loc in ship.positions:
			print("You missed! Try again.")

		

		#shoot and validate function
		#validate shoot loc function unless you can use previous function
		#if not valid, call shoot and validate
		#if valid, determine if it's a miss or hit (or sunk) function?
		#if miss, print board, add to player.miss
		#if hit, print boaard, add to player.hit then determine if it has sunk ship
		# and whether he has won the game. Check all ship health? 




if __name__ == "__main__":
	game()