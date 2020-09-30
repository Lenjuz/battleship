import json
import os
from random import randint

'''
Few things to keep in consideration:
------------------
    HIT = "X"
    MISS = "O"
    SHIP = "s"
    OCEAN = "-"
------------------
'''

# Global variables and settings
player_board = []
enemy_board = []
game_going = True
file_list = []

current_player = 'Player'
allowed_direction = 'HV'
allowed_choices = 'NL'
allowed_saves = 'CS'

player_attempts = 0
computer_attempts = 0
player_life = 14
computer_life = 14



# Our ship types and their corrensponding length
ships = {"Battleship": 5,
		"Aircraft carrier": 4,
 		"Destroyer": 3,
		"Submarine": 2}

# Adding to our empty board with ocean tiles
for rows in range(10):
    player_board.append([])
    enemy_board.append([])
    for columns in range(10):
        player_board[rows].append('-')
        enemy_board[rows].append('-')


# Used the zip method from:
# https://stackoverflow.com/questions/53446425/creating-a-row-of-numbers-letters-in-my-python-battleship-game
# Display our board with numbers outside to help reference coordinates
def print_player_board(player_board):
    print("Your board!")
    print(" ".join(" 0123456789"))
    for rownumb, row in zip("0123456789", player_board):
        print(rownumb, " ".join(row))


# Separate the top and bottom board with an ugly line
def random_seperation():
    print(f'--------------------------------------')
    

# Same print as our board but this one is where we shoot!
def print_enemy_board(enemy_board):
    print("Enemy board!")
    print(" ".join(" 0123456789"))
    for rownumb, row in zip("0123456789", enemy_board):
        str = rownumb + " " + " ".join(row)
        str = str.replace("s", "-")
        print(str) 


# Things before we start the game such as placing our ships, enemy ships and others
def initialise():

    display()

    # Take one ship at a time and call our ship placement function
    for i in ships.keys():
        print(f'\nCurrently placing the "{i}" with size of {ships[i]} tiles\n')
        while not ship_placement(ships[i]):
            print(f'Try again!')

    savegame()
    choice()
    display()
    print("\nEnemy ships have been placed hidden on the bottom board!\nYour ships have been placed on the top board!\n")
    input("\nPress enter to START...\n")


# Just packed all display functions into one to be called easier
def display():
    print_player_board(player_board)
    random_seperation()
    print_enemy_board(enemy_board)


# Prompt on save our strategic ship layout
def savegame():
    global allowed_saves, file_list
    
    while True:
        try:
            saveprompt = input("Would you like to continue without saving or save your ship layout for later use for the computer?\nC = Continue\nS = Save\n\n")
            if saveprompt in allowed_saves and len(saveprompt) != 0 and len(saveprompt) == 1:
                break
            else:
                print("\nNot an option, choose either C or S!\n")

        except:
            print("INVALID INPUT!")

    if saveprompt == "S":
        name_file = input("What would you like to name this save?\n")
        file_list.append(name_file)
        filename = f'{name_file}.json'

        with open(filename, 'w') as f:
            json.dump(player_board, f)
       
    elif saveprompt == "C":
        pass

    else:
        print("Incase you somehow got here ERROR!?")
        

# Prompt to have random computer board or loud our saved ones
def choice():
    global allowed_choices, file_list
    while True:
        try:
            choice = input("\nWould you like to play against a new random computer board or load one of the previous saved ones?\nN = New\nL = Load\n\n")
            if choice in allowed_choices and len(choice) != 0 and len(choice) == 1:
                break
            else:
                print("\nNot an option, choose either L or N!\n")

        except:
            print("INVALID INPUT!")

    # IMPORTANT! If you choose this you get a random ship placement for the computer!
    if choice == "N":
        place_computer()

    #IMPORTANT! If you choose this you will load from a file to convert into the computer board!
    elif choice == "L":
        load_game()
        

def load_game():
    global enemy_board
    print(f'Incase you have saved the board now here is the name {file_list}')
    while True:
        try:
            loadinput = input('What board file would you like to load? If you dont remember the name there is a "standard" file to load to continue\n')
            filename = f'{loadinput}.json'
            if os.path.exists(filename):
                with open(filename) as r:
                    enemy_board = json.load(r)
                    break
            

        except FileNotFoundError:
            print("No file like that exists!")


# If chosen in function choices() place computer ships randomly
def place_computer():
    for i in ships.keys():
        while not computer_placement(ships[i]):
            pass


# This is the game itself, we are taking turns to shoot at each others boards whoever sinks all the opponents ships wins!
def game_start():
    global game_going
    while game_going == True:

        player_turn(enemy_board)
        computer_turn(player_board)
        win_condition()
        

# Inputs for ship directions, coordinates and finally check/place using that information
def ship_placement(length):
    while True:
        try:
            ship_direction = input("Choose direction of ship with: \nH = Horizontal\nV = Vertical \n\n")
            if ship_direction in allowed_direction and len(ship_direction) != 0 and len(ship_direction) == 1:
                break
            else:
                print("Try again...")
        except:
            print("INVALID INPUT!\n")
  
    while True:
        try:
            ship_row = input("\nChoose a Y-coordinate to put your ship in 0-9:\n")
            ship_row = int(ship_row)
            
            if ship_row in range(0, 10):
                break
            else:
                print("That is outside the board bounds!")

        except:
            print("INVALID INPUT!\n")

    while True:
        try:
            ship_col = input("\nChoose a X-coordinate to put your ship in 0-9:\n")
            ship_col = int(ship_col)

            if ship_col in range(0, 10):
                break
            else:
                print("That is outside the board bounds!")

        except:
            print("INVALID INPUT!\n")

    
    # Error if not valid placement location
    try:
        valid_placement = check_placement(player_board, ship_row, ship_col, ship_direction, length)
    except:
        print("INVALID PLACEMENT!")
        return False

    # Placing ship if valid placement location
    if valid_placement:
        place_ship(player_board, ship_row, ship_col, ship_direction, length)
        print_player_board(player_board)

        return valid_placement


# Our function to check the placement before giving a green light on placing ships
def check_placement(board, ship_row, ship_col, ship_direction, length):
    valid = True

    for i in range(length):
        if ship_direction == "V":
            if check_coord(board, ship_row + i, ship_col) != "-":
                print("\nThis place is occupied or out of bounds!\n")
                valid = False
                break

        elif ship_direction == "H":
            if check_coord(board, ship_row, ship_col + i) != "-":
                print("\nThis place is occupied or out of bounds!\n")
                valid = False
                break

    return valid


# This function is used to check the board if its in range
def check_coord(board, rows, shoot_col):
    if rows not in range(len(board)):
        return "#"
    if shoot_col not in range(len(board)):
        return "#"

    return board[rows][shoot_col]


# After we got a valid confirmation on placement and check we lay out the ship!
def place_ship(board, ship_row, ship_col, ship_direction, length):
    for i in range(length):
        if ship_direction == "V":
            board[ship_row + i][ship_col] = "s"
        elif ship_direction == "H":
            board[ship_row][ship_col + i] = "s"


# Our turn to shoot and if we hit we go again, the turn is only over once we miss!
def player_turn(board):
    global player_attempts, computer_life
    print(f'{current_player} turn')
    while True:
        while True:
            try:
                shoot_row = input("Which row do you want to target 0-9: ")
                shoot_row = int(shoot_row)

                if shoot_row in range(0, 10):
                    break
                else:
                    print("That is outside the board bounds!")

            except:
                print("INVALID INPUT!\n")

        while True:
            try:
                shoot_col = input("Which column do you want to target 0-9: ")
                shoot_col = int(shoot_col)

                if shoot_col in range(0, 10):
                    break
                else:
                    print("That is outside the board bounds!")

            except:
                print("INVALID INPUT!\n")

    # We use our working check_coord function to look at the coordinates for already miss/hit
        if check_coord(enemy_board, shoot_row, shoot_col) not in ("O", "X"):
            break

        else:
            print("You have already shot here!")

    # Messy but it works for now...
    if check_coord(enemy_board, shoot_row, shoot_col) == "s":
        enemy_board[shoot_row][shoot_col] = "X"
        display()
        print("Player HITS and takes another turn!")
        computer_life -= 1
        player_attempts += 1
        player_turn(enemy_board)
    else:
        enemy_board[shoot_row][shoot_col] = "O"
        display()
        print("\nPlayer MISSED!\n")
        player_attempts += 1
        change_turn()
        return enemy_board
    
    
# We change turn between player and computer until someone has won.
def change_turn():
    global current_player
    if current_player == 'Player':
        current_player = 'Computer'
    elif current_player == 'Computer':
        current_player = "Player"
    return


# Computer takes it's random turns on our board and follows the same rules as we do incase it hits/miss.
def computer_turn(board):
    global computer_attempts, player_life
    print(f'{current_player} turn')
    input("Press enter to continue...")
    
    comp_shootrow = randint(0, 9)
    comp_shootcol = randint(0, 9)

    while player_board[comp_shootrow][comp_shootcol] == "X" or "O":
        comp_shootrow = randint(0, 9)
        comp_shootcol = randint(0, 9)  
        if player_board[comp_shootrow][comp_shootcol] == "s" or "-":
            break

    if player_board[comp_shootrow][comp_shootcol] == "s":
        player_board[comp_shootrow][comp_shootcol] = "X"
        display()
        print("Computer HITS and takes another turn")
        computer_attempts += 1
        player_life -= 1
        computer_turn(board)
        

    else:
        player_board[comp_shootrow][comp_shootcol] = "O"
        display()
        print("\nComputer MISSED!\n")
        computer_attempts += 1
        change_turn()
        return player_board


# Similar to our ship placement but each input is replaced by randomization
def computer_placement(length):

    enemy_direction = randint(0, 1)
    if enemy_direction == 0:
        enemy_direction = "H"
    elif enemy_direction == 1:
        enemy_direction = "V"

    x = randint(0, 9)
    y = randint(0, 9)

    try:
        valid_placement = check_placement(enemy_board, x, y, enemy_direction, length)
    except:
        return False

    if valid_placement:
        place_ship(enemy_board, x, y, enemy_direction, length)

    return valid_placement

# If someone finally sinks all of the opponents ships they win and it displays amount of attempts/shots
def win_condition():
    global game_going, player_life, computer_life

    if computer_life <= 0:
        current_player = "Player"
        print(f'{current_player} has WON! and it only took {player_attempts - 1} shots!\n')
	input("Press enter to close program thank you for playing!")

        filename = 'victorylog.txt'
        with open('victorylog.txt', 'a+') as f:
            f.write(f'\n{current_player} WON! And it took {player_attempts - 1} shots!\n')

        game_going = False

    elif player_life <= 0:
        current_player = "Computer"
        print(f'{current_player} has WON! and it only took {computer_attempts - 1} shots!\n')
	input("Press enter to close program thank you for playing!")

        filename = 'victorylog.txt'
        with open('victorylog.txt', 'a+') as f:
            f.write(f'\n{current_player} WON! And it took {player_attempts - 1} shots!\n')

        game_going = False



initialise()
game_start()


    

