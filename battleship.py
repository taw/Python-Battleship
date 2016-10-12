from player import Player
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
	location = input("{}, select location of the {} ({} spaces): ".format(player, ship_type, ship_size))
	if is_loc_valid(location):
		return location
	else:
		print("Error! Must have letters A - J and numbers 1 - 10. For example: G7")
		return prompt_location(player, ship_type, ship_size)


def is_loc_valid(location):
	if len(location) == 2 and ord(location[0].lower()) in range(ord("a"), ord("k")) and int(location[1]) in range(0, 11):
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
		if int(location[1]) + ship_size <= 10:
			return True
		else:
			return False

def get_ship_locs(location, orientation, ship_size):
	'''Returns a tuple of all the coordinates the ship
	occupies in the board'''
	ship_locs = []
	col_ind = ord(location[0].lower()) - ord("a")
	row_ind = int(location[1]) - 1
	index = 0
	if orientation == "h":
		for i in range(ship_size):
			ship_locs.append((col_ind + index, row_ind))
			index += 1
	else:
		for i in range(ship_size):
			ship_locs.append((col_ind, + row_ind + index))
			index += 1
	return ship_locs

def ship_overlap(input_locs, ship_locs):
	for ships in input_locs:
		for ships2 in ship_locs:
			if ships in ships2.positions:
				return True
			

def place_ships(player):
	print("PLACE YOUR SHIPS ON THE BOARD \n")
	player.board.print_board()
	for i in range(len(player.ships)):
		location = prompt_location(player.name, player.ships[i].ship_type, player.ships[i].size)
		orientation = prompt_orientation()
		ship_locs = get_ship_locs(location, orientation, player.ships[i].size)
		while True: 
			if is_orientation_valid(orientation, location, player.ships[i].size):
				if not ship_overlap(ship_locs, player.ships):
					player.ships[i].positions.extend(ship_locs)
					break
				else:
					print("Error! Ship overlaps location of another ship. Choose another location.")
					location = prompt_location(player.name, player.ships[i].ship_type, player.ships[i].size)
					orientation = prompt_orientation()
			else:
				print("Error! Ship does not fit the board. Enter another location or orientation")
				location = prompt_location(player.name, player.ships[i].ship_type, player.ships[i].size)
				orientation = prompt_orientation()
		ship_overlap(ship_locs, player.ships)
		player.ships[i].orientation = orientation
	

		
		print(ship_locs)
		print(player.ships[i].positions)

def game():
	print(ascii_art())
	print("Player 1")
	Player1 = Player()
	print("Player 2")
	Player2 = Player()
	

	place_ships(Player2)
	print(Player2.ships[0].positions)
	print(Player2.ships[1].positions)
	print(Player2.ships[2].positions)
	print(Player2.ships[3].positions)



if __name__ == "__main__":
	game()