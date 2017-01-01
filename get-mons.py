"""
"Main menu" for the Dex.
Can navigate to Pokemon, Item, Ability, Move searches, along with Catching Sim and Stat @ Level.
"""

from abilitymap import *
from statsatlevel import *
from catchingsim import *


def findMon(numname):
    """
    Finds a Pokemon given a number or name.
    :str numname: Either a number or name of a Pokemon.
    :return: None
    """
    try:
        int(numname[0]) #Indicates user is looking for a number
        number = numname
        try:
            name = num_to_name[number].lower()
        except IndexError:
            name = numname.lower()
        except KeyError:
            print("Nothing found for this number.")
            return
        print(mons_by_num[numname])
    except ValueError:
        numname = numname.lower()
        name = numname
        if numname not in mons_by_name:
            print("Nothing found for this name.")
            return
        print(mons_by_name[numname])

    try:
        # String together all the possible abilities the Pokemon can have
        ability_mon = ""
        length = len(mon_to_abilities[name])
        for item in mon_to_abilities[name]:
            if mon_to_abilities[name][length-1] == item:
                ability_mon += item.title()
            else:
                ability_mon += item.title() + ", "
        else:
            print("This Pokemon's possible abilities are: " + ability_mon)
    except KeyError:
        pass

def findAbility(ability):
    """
    Finds the ability and description of an ability.
    :str ability: ability name
    :return: None
    """
    ability = ability.lower()
    if ability not in abilities:
        print("Ability not found.")
        return
    print(abilities[ability])

    # String all Pokemon that can have an ability together
    mon_ability = ""
    length = len(ability_to_mons[ability])
    for item in ability_to_mons[ability]:
        try:
            for num in [6, 12, 18, 24, 30, 36, 42, 48]: # Break the line every so often to eliminate overflow.
                if ability_to_mons[ability][num] == item:
                    mon_ability += "\n                        "
        except IndexError:
            pass
        if ability_to_mons[ability][length-1] == item:
            mon_ability += item.title()
        else:
            mon_ability += item.title() + ", "
    print("Pokemon with " + ability.title() + ": " + mon_ability)

def findItem(item):
    """
    Find items that contain a certain phrase.
    :str item: Phrase that is used to search for items.
    :return: None
    """
    counter = 0
    print("Showing all items containing " + item.title() + ": ")
    print()
    for object in items:
        if item in object:
            print(items[object])
            counter += 1
    if counter == 0:
        print("Item not found.")

def findMove(move):
    """
    Finds a move or TM given a phrase to search in.
    :str move: Phrase to search for moves.
    :return: None
    """
    counter = 0
    try: # TM search
        if move[0] == "0":
            number = int(move[1])
        else:
            number = int(move)
        print("TM " + tm[number].tm + ":")
        print(tm[number])
    except KeyError:
        print("TM not found.")
    except ValueError:
        print("Showing all moves containing " + move.title() + ": ")
        print()
        for item in moves:
            if move in item:
                print(moves[item])
                print()
                counter += 1
        if counter == 0:
            print("Move not found.")



def init(debug):
    """
    Initializes the program and loads everything into memory.
    :return: None
    """
    print("Initializing... Please wait.")
    first_time = time.clock()
    if debug:
        mon_time = time.clock()
        load_mons()
        new_mon = time.clock()
        print("Mons: " + str(int(new_mon-mon_time)))
        mon_time = time.clock()
        load_abilities()
        new_mon = time.clock()
        print("Abl: " + str(int(new_mon-mon_time)))
        mon_time = time.clock()
        load_moves()
        new_mon = time.clock()
        print("Moves: " + str(int(new_mon-mon_time)))
        mon_time = time.clock()
        load_items()
        new_mon = time.clock()
        print("Items: " + str(int(new_mon-mon_time)))
        mon_time = time.clock()
        ability_to_mon()
        new_mon = time.clock()
        print("AbilityToMon: " + str(int(new_mon-mon_time)))
    else:
        load_abilities()
        load_moves()
        load_items()
        ability_to_mon()
    get_rates()
    get_water_bug()
    done_time = time.clock()
    total_time = done_time-first_time

    print("Done! Total time taken: " + str(int(total_time)))


def main():
    """
    Main Menu, leads the user to various functions of the program.
    :return: None
    """
    init(True)
    while True:
        search = input("Welcome to Pythondex!\n1. Search for Pokemon\n2. Search for Abilities\n"
                       "3. Search for Items\n4. Search for Moves\n5. Catching Simulator\n"
                       "6. Calculate Stats at Level\nLeave blank to exit program.\nYour Selection: ")
        if search == "1":
            while True:
                print()
                numname = input("Enter name or number of Pokemon (Leave blank to exit): ")
                if numname == '':
                    break
                findMon(numname)
        elif search == "2":
            while True:
                print()
                ability = input("Enter ability (Leave blank to exit): ")
                if ability == '':
                    break
                findAbility(ability)
        elif search == "3":
            while True:
                print()
                item = input("Enter Item: (Leave blank to exit): ")
                if item == '':
                    break
                findItem(item)
        elif search == "4":
            while True:
                print()
                move = input("Enter Move: (Leave blank to exit): ")
                if move == '':
                    break
                findMove(move)
        elif search == "5":
            print()
            sim()
        elif search == "6":
            print()
            stat()
        elif search.lower() == "debug":
            # Small debug menu for checking values of things.
            while True:
                print()
                selection = input("1. Print list of mons\n2. Print list of abilities\n"
                                  "3. Print list of moves\n4. Print list of items\n")
                if selection == "1":
                    for name in names:
                        print(name)
                elif selection == "2":
                    for ability in abilities:
                        print(ability)
                elif selection == "3":
                    for move in moves:
                        print(move)
                elif selection == "4":
                    for item in items:
                        print(item)
                elif selection == "":
                    break
        elif search == "":
            break
        else:
            print("Invalid command. ")
            print()
            continue



if __name__ == "__main__":
    main()



