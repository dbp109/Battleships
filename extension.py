from battleships import *
from os import system, name

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

def main():
    current_fleet = randomly_place_all_ships()
    game_over = False
    shots = 0

    ocean = [['O' for x in range(10)] for x in range(10)]
    missed = set()
    while not game_over:
        loc_str = input("Enter row and column to shoot (separated by space) or type 'q' to quit: ")
        if loc_str.lower() == "q":
            break
        loc_str = loc_str.split()
        current_row = int(loc_str[0])
        current_column = int(loc_str[1])
        shots += 1
        clear()
        if check_if_hits(current_row, current_column, current_fleet):
            (current_fleet, ship_hit) = hit(current_row, current_column, current_fleet)
            print("You have a hit!")
            if is_sunk(ship_hit):
                print("You sank a " + ship_type(ship_hit) + "!")
        else:
            print("You missed!")
            missed.add((current_row, current_column))
        for i in missed:
            i = list(i)
            ocean[i[0]][i[1]] = "-"
        for ship in current_fleet:
            for i in ship[4]:
                if not is_sunk(ship):
                    ocean[i[0]][i[1]] = "*"
                if ship_type(ship) == "submarine" and is_sunk(ship):
                    ocean[i[0]][i[1]] = "S"
                if ship_type(ship) == "destroyer" and is_sunk(ship):
                    ocean[i[0]][i[1]] = "D"
                if ship_type(ship) == "cruiser" and is_sunk(ship):
                    ocean[i[0]][i[1]] = "C"
                if ship_type(ship) == "battleship" and is_sunk(ship):
                    ocean[i[0]][i[1]] = "B"
        print("")
        print("")
        print("      0 1 2 3 4 5 6 7 8 9")
        print("      -------------------")
        for i in range(len(ocean)):
            print(i, " | ", *ocean[i])

        if not are_unsunk_ships_left(current_fleet): game_over = True

    print("Game over! You required", shots, "shots.")


if __name__ == '__main__': #keep this in
    main()



