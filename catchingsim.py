"""
Provides a simulation of catching a Pokemon, using a specific type of ball, and any status conditions.
"""

from math import *
from random import *
import time

from loaddex import *

catch_rates = {}
water = []
bug = []

def get_rates():
    """
    Generates a dictionary of Pokemon and their catch rates.
    :return: None
    """
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_catch_rate")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    mon = soup.find('table', class_='roundy').contents[1].contents[1].contents[1]

    counter = 3
    while counter <= 1605:
        name = mon.contents[counter].contents[5].contents[1].contents[0]
        rate = mon.contents[counter].contents[7].contents[0].strip().rstrip('\n')
        for char in '*':
            rate = rate.replace(char, '')
        lowername = name.lower()
        catch_rates[lowername] = rate
        counter += 2

def get_water_bug():
    """
    Generates two lists, each containing names of Pokemon that are water or bug type. Duplicates
    are excluded.
    :return: None
    """
    r  = requests.get("http://www.serebii.net/pokedex-sm/water.shtml")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    counter = 5
    mon = soup.find('table', class_='dextable')

    while counter <= 290:
        name = mon.contents[counter].contents[5].contents[1].contents[0]
        if name in water:
            pass
        else:
            water.append(name)
        if counter == 193:
            counter -= 1  #Serebii has weird formatting from Rotom on, must have forgotten a new line.
        counter += 2

    r  = requests.get("http://www.serebii.net/pokedex-sm/bug.shtml")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    counter = 5
    mon = soup.find('table', class_='dextable')

    while counter <= 173:
        name = mon.contents[counter].contents[5].contents[1].contents[0]
        if name in [bug, water]:
            pass
        else:
            bug.append(name)
        counter+=2



def ball_bonus(ball, pokemon, level):
    """
    Returns the multiplier for the ball used.
    Does not use any Apricorn balls.
    :str ball: Either the first word of the ball or the full name.
    :str pokemon: Used for Net ball.
    :int level: Used for Nest ball.
    :float return: bonus multiplier.
    """
    ball = ball.lower()
    ball = ball.split(' ')
    ball = ball[0] #This gets the first word of the string.

    pokemon = pokemon.lower()

    if ball in ["poke", "premier", "luxury", "heal", "cherish"]:
        return 1
    elif ball in ["great", "safari"]:
        return 1.5
    elif ball == "ultra":
        return 2
    elif ball in ["master", "park", "dream"]:
        return 0 # Catches without fail
    elif ball == "net":
        if pokemon in [water, bug]:
            return 3
        else:
            return 1
    elif ball == "nest":
        nest = ((40-level)/10)
        if nest <= 1:
            return 1 # Minimum of 1x
        else:
            return nest
    elif ball == "repeat":
        caught = input("Have you caught " + pokemon + " before? (y/n) ").lower()
        if caught == "y":
            return 3
        else:
            return 1
    elif ball == "timer":
        turns = int(input("Number of turns in the battle? "))
        if turns > 10:
            turns = 10
        return (1 + turns * (1229/4096))
    elif ball == "dive":
        dive = input("Are you diving, surfing, or fishing? (y/n) ").lower()
        if dive == "y":
            return 3.5
        else:
            return 1
    elif ball == "dusk":
        dusk = input("Night or cave? (y/n) ").lower()
        if dusk == "y":
            return 3.5
        else:
            return 1
    elif ball == "quick":
        quick = input("First turn of battle? (y/n) ").lower()
        if quick == "y":
            return 5
        else:
            return 1
    elif ball == "beast":
        if pokemon in ["nihilego", "buzzwole", "pheromosa",
                       "xurkitree", "celesteela", "kartana", "guzzlord"]:
            return 5
        else:
            return .1
    else:
        print("Ball not found, try again.")
        return -1


def shakecheck(a, b):
    """
    Performs 4 shake tests to determine if the pokemon will be caught.
    :param a: "a" from the catch rate formula
    :param b: "b" from the catch rate formula
    :return: None
    """
    b = floor(b)
    percent = ((b/65536)**4)*100
    shakes = 1
    if a >= 255: # Guaranteed catch
        percent = 100
        print("Catch rate: " + "{:>4.2f}".format(percent) + "%")
        print("Caught!")
    else:
        while shakes < 5: # 4 Shake tests
            rand = randint(0, 65536) # Games generate a random integer, if higher than b, catch fails.
            if rand >= b:
                print("Catch rate: " + "{:>4.2f}".format(percent) + "%")
                print("Missed!")
                return
            else:
                if shakes > 1:
                    print("Shake...") # Suspense
                    time.sleep(1)
                shakes += 1
        print("Caught!")
        print("Catch rate: " + "{:>4.2f}".format(percent) + "%")




def sim():
    while True:
        try:
            pokemon = input("Pokemon (Leave blank to exit): ").lower()
            if pokemon == '':
                return
            basehp = mons_by_name[pokemon].hp
            rate = catch_rates[pokemon]
            level = int(input("Level: "))
            if level > 100 or level < 1:
                print("Level must be between 1 and 100.")
                print()
                continue
            hp_max = floor((((2*basehp) * level)/100)+level+10)
            current_hp = input("Percent of HP remaining? (Enter 0 for 1hp) ").rstrip('%')
            if int(current_hp) > 100 or int(current_hp) < 0:
                print("HP must be between 0 and 100.")
                print()
                continue
            if current_hp == "0":
                current_hp = 1
            else:
                current_hp = (int(current_hp)/100)*hp_max
            ball = input("Type of ball: ")
            bonus = ball_bonus(ball, pokemon, level)
            if bonus == -1:
                print()
                continue
            status = input("(F)reeze, (S)leep, (P)aralyze, or (N)one? ").lower()
            if status in ['f', 's']:
                status = 2.5
            elif status == 'p':
                status = 2
            else:
                status = 1

            a = (((((3 * int(hp_max)) - (2 * int(current_hp))) * int(rate) * float(bonus))/(3 * int(hp_max))) * int(status))
            if bonus == 0:
                a = 256 # Master, park, or dream balls
            b = (65536 / ((255/a)**0.1875)) # Gen 6+
            #b = 65536 / sqrt(sqrt(255/a)) # Gen 5
            shakecheck(a, b)
            print()
        except KeyError:
            print("Pokemon not found.")
            print()
            continue
        except ValueError:
            print("Error: Value must be a number.")
            print()
            continue

if __name__ == "__main__":
    get_water_bug()
    get_rates()
    load_mons()
    sim()
