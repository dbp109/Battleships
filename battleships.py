from random import randint
import os

def is_sunk(ship):
    '''returns Boolean value, which is True if ship is sunk and False otherwise'''
    if ship_type(ship) == "submarine" and len(ship[4]) == 1:
        return True
    elif ship_type(ship) == "destroyer" and len(ship[4]) == 2:
        return True
    elif ship_type(ship) == "cruiser" and len(ship[4]) == 3:
        return True
    elif ship_type(ship) == "battleship" and len(ship[4]) == 4:
        return True
    else: return False

def ship_type(ship):
    '''returns one of the strings "battleship", "cruiser", "destroyer",
    or "submarine" identifying the type of ship'''
    if ship[3] == 1:
        return "submarine"
    elif ship[3] == 2:
        return "destroyer"
    elif ship[3] == 3:
        return "cruiser"
    elif ship[3] == 4:
        return "battleship"

def is_open_sea(row, column, fleet):
    '''checks if the square given by row and column neither contains nor is adjacent
    (horizontally, vertically, or diagonally) to some ship in fleet. Returns Boolean
    True if so and False otherwise'''
    for ship in fleet:
        for i in range(ship[3]):
            if ship[2]:
                old_row = ship[0]
                old_column = ship[1] + i
            else:
                old_row = ship[0] + i
                old_column = ship[1]
            if old_row == row and old_column == column:
                return False
            if old_row == row-1 and old_column == column-1:
                return False
            if old_row == row-1 and old_column == column:
                return False
            if old_row == row-1 and old_column == column+1:
                return False
            if old_row == row and old_column == column-1:
                return False
            if old_row == row and old_column == column+1:
                return False
            if old_row == row+1 and old_column == column-1:
                return False
            if old_row == row+1 and old_column == column:
                return False
            if old_row == row+1 and old_column == column+1:
                return False
    return True

def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    '''checks if addition of a ship, specified by row, column, horizontal, and length
    as in ship representation above, to the fleet results in a legal arrangement
    (see the figure above). If so, the function returns Boolean True and it returns
    False otherwise. This function makes use of the function is_open_sea'''
    for i in range(length):
        if column + i < 0 or column + i > 9 or row + i < 0 or row + i > 9:
            return False
        if horizontal and not is_open_sea(row, column + i, fleet):
            return False
        elif not horizontal and not is_open_sea(row + i, column, fleet):
            return False
    return True

def place_ship_at(row, column, horizontal, length, fleet):
    '''returns a new fleet that is the result of adding a ship, specified by row, column,
    horizontal, and length as in ship representation above, to fleet. It may be assumed that
    the resulting arrangement of the new fleet is legal'''
    ship = (row, column, horizontal, length, set())
    fleet.append(ship)
    return fleet

def randomly_place_all_ships():
    '''returns a fleet that is a result of a random legal arrangement of the 10 ships in
    the ocean. This function makes use of the functions ok_to_place_ship_at and place_ship_at'''
    fleet = []
    length = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    while len(fleet) < 10:
        row = randint(0,9)
        column = randint(0, 9)
        horizontal = bool(randint(0, 1))
        length_pop = length.pop()
        if ok_to_place_ship_at(row, column, horizontal, length_pop, fleet):
            place_ship_at(row, column, horizontal, length_pop, fleet)
        else:
            length.append(length_pop)
    return fleet

def check_if_hits(row, column, fleet):
    '''returns Boolean value, which is True if the shot of the human player at the square
    represented by row and column hits any of the ships of fleet, and False otherwise'''
    for ship in fleet:
        if (row, column) in ship[4]:
            return False
        if ship[2]:
            for i in range(ship[3]):
                new_row = ship[0]
                new_column = ship[1] + i
                if row == new_row and column == new_column:
                    return True
        if not ship[2]:
            for i in range(ship[3]):
                new_row = ship[0] + i
                new_column = ship[1]
                if row == new_row and column == new_column:
                    return True
    return False

def hit(row, column, fleet):
    '''returns a tuple (fleet1, ship) where ship is the ship from the fleet fleet that
    receives a hit by the shot at the square represented by row and column, and fleet1
    is the fleet resulting from this hit. It may be assumed that shooting at the square
    row, column results in of some ship in fleet'''
    fleet1 = [list(s) for s in fleet]
    for ships in fleet:
        if ships[2]:
            for i in range(ships[3]):
                new_row = ships[0]
                new_column = ships[1] + i
                if row == new_row and column == new_column:
                    ships[4].add((new_row, new_column))
                    ship = ships
        if not ships[2]:
            for i in range(ships[3]):
                new_row = ships[0] + i
                new_column = ships[1]
                if row == new_row and column == new_column:
                    ships[4].add((new_row, new_column))
                    ship = ships
    fleet1 = [tuple(s) for s in fleet]
    return (fleet1, ship)

def are_unsunk_ships_left(fleet):
    '''returns Boolean value, which is True if there are ships in the fleet that are
    still not sunk, and False otherwise'''
    count = 0
    for ship in fleet:
        if is_sunk(ship):
            count += 1
    if count == 10:
        return False
    else:
        return True

def main():
    '''returns nothing. It prompts the user to call out rows and columns of shots and
    outputs the responses of the computer (see General Idea of Assignment) iteratively
    until the game stops. Our expectations from this function: (a) there must be an option
    for the human player to quit the game at any time, (b) the program must never crash
    (i.e., no termination with Python error messages), whatever the human player does.
    Note that there is an indicative implementation of main() to help you start working,
    but it does not satisfy the expectations above and you should improve or entirely redo it.'''
    current_fleet = randomly_place_all_ships()
    game_over = False
    shots = 0

    while not game_over:
        loc_str = input("Enter row and column to shoot (separated by space) or type 'q' to quit: ")
        if loc_str.lower() == "q":
            break
        loc_str = loc_str.split()
        current_row = int(loc_str[0])
        current_column = int(loc_str[1])
        shots += 1

        if check_if_hits(current_row, current_column, current_fleet):
            print("You have a hit!")
            (current_fleet, ship_hit) = hit(current_row, current_column, current_fleet)
            if is_sunk(ship_hit):
                print("You sank a " + ship_type(ship_hit) + "!")
        else:
            print("You missed!")

        if not are_unsunk_ships_left(current_fleet): game_over = True

    print("Game over! You required", shots, "shots.")


if __name__ == '__main__': #keep this in
   main()
