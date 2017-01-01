from math import *

from loaddex import *


def calculate_stats(pokemon, level, iv, ev, nature):

    """
    Calculates a stat spread at a certain level, given IVs and EVs.
    :str pokemon: name of Pokemon
    :str level: Target level
    :str iv: set of IV's
    :str ev: set of EV's
    :str nature: Given nature
    :return:
    """
    pokemon = pokemon.lower()
    ivlist = iv.split("/")
    evlist = ev.split("/")
    ev_total = 0
    if len(ivlist)!= 6 or len(evlist) != 6:
        return -3
    try:
        for item in evlist:
            ev_total += int(item)
        if ev_total > 510:
            return -4

        level = int(level)

        hp_iv = int(ivlist[0])
        hp_ev = int(evlist[0])

        attack_iv = int(ivlist[1])
        attack_ev = int(evlist[1])

        defense_iv = int(ivlist[2])
        defense_ev = int(evlist[2])

        spattack_iv = int(ivlist[3])
        spattack_ev = int(evlist[3])

        spdefense_iv = int(ivlist[4])
        spdefense_ev = int(evlist[4])

        speed_iv = int(ivlist[5])
        speed_ev = int(evlist[5])

        for item in [hp_iv, attack_iv, defense_iv, spattack_iv, spdefense_iv, speed_iv]:
            if item < 0 or item > 31:
                return -1
        for item in [hp_ev, attack_ev, defense_ev, spattack_ev, spdefense_ev, speed_ev]:
            if item < 0 or item > 252:
                return -2

    except ValueError:
        print("Values must be numbers. ")
        return

    new_stats = []
    bonuses = get_nature(nature)
    base_hp = mons_by_name[pokemon].hp
    new_hp = floor(((2 * base_hp + hp_iv + floor(hp_ev/4)) * level) / 100) + level + 10
    if pokemon == "Shedinja":
        new_hp = 1
    new_stats.append(new_hp)
    base_attack = mons_by_name[pokemon].attack
    new_attack = floor((floor(((2 * base_attack + attack_iv + floor(attack_ev/4)) * level)/100)+5) * bonuses[0])
    new_stats.append(new_attack)
    base_defense = mons_by_name[pokemon].defense
    new_defense = floor((floor(((2 * base_defense + defense_iv + floor(defense_ev/4)) * level)/100)+5) * bonuses[1])
    new_stats.append(new_defense)
    base_spattack = mons_by_name[pokemon].spattack
    new_spattack = floor((floor(((2 * base_spattack + spattack_iv + floor(spattack_ev/4)) * level)/100)+5) * bonuses[2])
    new_stats.append(new_spattack)
    base_spdefense = mons_by_name[pokemon].spdefense
    new_spdefense = floor((floor(((2 * base_spdefense + spdefense_iv + floor(spdefense_ev/4)) * level)/100)+5) * bonuses[3])
    new_stats.append(new_spdefense)
    base_speed = mons_by_name[pokemon].speed
    new_speed = floor((floor(((2 * base_speed + speed_iv + floor(speed_ev/4)) * level)/100)+5) * bonuses[4])
    new_stats.append(new_speed)

    return new_stats


def get_nature(nature):
    """
    Attack = [0]
    Defense = [1]
    Sp. Attack = [2]
    Sp. Defense = [3]
    Speed = [4]
    """
    nature_bonuses = [1, 1, 1, 1, 1]
    nature = nature.lower()
    if nature in ["lonely", "brave", "adamant", "naughty"]:
        nature_bonuses[0] += .1
    if nature in ["bold", "timid", "modest", "calm"]:
        nature_bonuses[0] -= .1
    if nature in ["bold", "relaxed", "impish", "lax"]:
        nature_bonuses[1] += .1
    if nature in ["lonely", "hasty", "mild", "gentle"]:
        nature_bonuses[1] -= .1
    if nature in ["modest", "mild", "quiet", "rash"]:
        nature_bonuses[2] += .1
    if nature in ["adamant", "impish", "jolly", "careful"]:
        nature_bonuses[2] -= .1
    if nature in ["calm", "gentle", "sassy", "careful"]:
        nature_bonuses[3] += .1
    if nature in ["naughty", "lax", "naive", "rash"]:
        nature_bonuses[3] -= .1
    if nature in ["timid", "hasty", "jolly", "naive"]:
        nature_bonuses[4] += .1
    if nature in ["brave", "relaxed", "quiet", "sassy"]:
        nature_bonuses[4] -= .1

    return nature_bonuses

def stat():
    while True:
        try:
            pokemon = input("Enter Pokemon (Leave blank to exit) : ")
            if pokemon == "":
                return
            if not pokemon.lower() in names:
                print("Pokemon not found.")
                print()
                continue
            level = int(input("Level: "))
            if level < 0 or level > 100:
                print("Level must be between 0 and 100.")
                print()
                continue
            iv = input("Enter IV's separated by / (Example: 1/2/3/4/5/6): ")
            ev = input("Enter EV's separated by / (Example: 0/4/0/252/0/252): ")
            nature = input("Enter nature: ")
            new_stats = calculate_stats(pokemon, level, iv, ev, nature)
            if new_stats == -1:
                print("IV's must be between 0 and 31.")
                continue
            elif new_stats == -2:
                print("EV's must be between 0 and 252.")
                continue
            elif new_stats == -3:
                print("Invalid number of IV's or EV's.")
                continue
            elif new_stats == -4:
                print("Invalid combination of EV's, must be below 510.")
                continue
            else:
                print("Stats of " + pokemon.title() + " at level " + str(level) + ":\n"
                      + "HP: " + str(new_stats[0]) + "\nAttack: " + str(new_stats[1])
                      + "\nDefense: " + str(new_stats[2]) + "\nSp. Attack: " + str(new_stats[3])
                      + "\nSp. Defense: " + str(new_stats[4]) + "\nSpeed: " + str(new_stats[5]))
        except ValueError:
            print("Error: Invalid Argument")
            continue

if __name__ == "__main__":
    load_mons()
    stat()