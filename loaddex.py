"""

"""

from bs4 import BeautifulSoup
import requests
from Pokemon import *


names = []
numbers = []
mons_by_num = {}
mons_by_name = {}
abilities = {}
num_to_name = {}
items = {}
movelist = []
moves = {}
tm = {}

def load_mons():
    """
    Generate two dictionaries, one by Pokemon name, and one by Pokemon number.
    :return: None
    """
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/"
                      "List_of_Pok%C3%A9mon_by_base_stats_(Generation_VII-present)")

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    mon = soup.find('table', class_='sortable roundy')

    counter = 3 # Bulbasaur starts at 3, everything else is +2 from the previous
    while counter <= 1807:
        number = mon.contents[counter].contents[1].contents[1].contents[0]
        if number in numbers:   # Used for multiple form Pokemon for easier finding by number
            newnumber = mon.contents[counter].contents[1].contents[1].contents[0] + ".a"
            if newnumber in numbers:
                newnumber = mon.contents[counter].contents[1].contents[1].contents[0] + ".b"
                if newnumber in numbers:
                    newnumber = mon.contents[counter].contents[1].contents[1].contents[0] + ".c"
            number = newnumber
        numbers.append(number)
        name = mon.contents[counter].contents[5].contents[1].contents[0]

        try:
            name = mon.contents[counter].contents[5].contents[3].contents[0] # These are used for alt forms.
            name = name.lower()
            name = name.replace("(", "")
            name = name.replace(")","")
            if name == "core":
                name = "minior core"
            elif name == "normal forme":
                name = "deoxys"
            elif name == "attack forme":
                name = "deoxys attack"
            elif name == "defense forme":
                name = "deoxys defense"
            elif name == "speed forme":
                name = "deoxys speed"
            elif name in ["heat rotom", "wash rotom", "frost rotom", "fan rotom", "mow rotom"]:
                name = name.split()
                newname = name[1] + " " + name[0]
                name = newname
            elif "cloak" in name:
                name = name.split()
                name = "wormadam " + name[0]
            elif name == "altered forme":
                name = "giratina"
            elif name == "origin forme":
                name = "giratina origin"
            elif name == "land forme":
                name = "shaymin"
            elif name == "sky forme":
                name = "shaymin sky"
            elif name == "standard mode":
                name = "darmanitan"
            elif name == "zen mode":
                name = "darmanitan zen"
            elif name == "incarnate forme":
                if number == "641":
                    name = "tornadus"
                elif number == "642":
                    name = "thundurus"
                elif number == "645":
                    name = "landorus"
            elif name == "therian forme":
                if number == "641.a":
                    name = "tornadus therian"
                elif number == "642.a":
                    name = "thundurus therian"
                elif number == "645.a":
                    name = "landorus therian"
            elif name == "aria forme":
                name = "meloetta"
            elif name == "pirouette forme":
                name = "meloetta pirouette"
            elif name == "shield forme":
                name = "aegislash shield"
            elif name == "blade forme":
                name = "aegislash blade"
            elif name in ["small size", "average size", "large size", "super size"]:
                name = name.split()
                if "710" in number:
                    name = "pumpkaboo " + name[0]
                else:
                    name = "gourgeist " + name[0]
            elif name in ["10% forme", "complete forme"]:
                name = name.split()
                name = "zygarde " + name[0]
            elif name == "midday form":
                name = "lycanroc midday"
            elif name == "midnight form":
                name = "lycanroc midnight"
            elif name == "school form":
                name = "wishiwashi school"
        except IndexError:
            pass
        if number == "032":
            name = "Nidoran M"
        if number == "029":
            name = "Nidoran F"

        names.append(name.lower())
        num_to_name[number] = name
        hp=int(mon.contents[counter].contents[7].contents[0].strip().rstrip('\n')) # Get HP
        attack=int(mon.contents[counter].contents[9].contents[0].strip().rstrip('\n')) # Get Attack
        defense=int(mon.contents[counter].contents[11].contents[0].strip().rstrip('\n')) # Get Defense
        spattack=int(mon.contents[counter].contents[13].contents[0].strip().rstrip('\n')) # Get Sp.Atk
        spdefense=int(mon.contents[counter].contents[15].contents[0].strip().rstrip('\n')) # Get Sp.Def
        speed=int(mon.contents[counter].contents[17].contents[0].strip().rstrip('\n')) # Get Speed
        counter += 2
        lowername = name.lower()
        mons_by_name[lowername] = Pokemon(number, name, hp, attack, defense, spattack, spdefense, speed)
        mons_by_num[number] = Pokemon(number, name, hp, attack, defense, spattack, spdefense, speed)


def load_abilities():
    """
    Loads all the abilities into a dictionary.
    key: name, value: description
    """
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/Ability")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    ability = soup.find('table', class_='sortable')
    counter = 3
    while counter <= 467:
        name = ability.contents[counter].contents[3].contents[1].contents[0]
        if name == "Cacophony":
            pass # Only found in one generation, not usable anywhere else
        else:
            ability_name = name
            name = name.lower()
            description = ability.contents[counter].contents[5].contents[0].strip().rstrip('\n')
            generation = ability.contents[counter].contents[7].contents[0].strip().rstrip('\n')
            abilities[name] = Ability(ability_name, description, generation)
        counter += 2


def load_items():
    r  = requests.get("http://pokemondb.net/item/all")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    item = soup.find('table', class_='data-table wide-table').contents[3]
    counter = 1
    while True:
        try:
            name = item.contents[counter].contents[1].contents[3].contents[0]
            if "Apricorn" in name:
                if "Blk" in name:
                    name = "Black Apricorn"
                elif "Blu" in name:
                    name = "Blue Apricorn"
                elif "Grn" in name:
                    name = "Green Apricorn"
                elif "Pnk" in name:
                    name = "Pink Apricorn"
                elif "Wht" in name:
                    name = "White Apricorn"
                elif "Ylw" in name:
                    name = "Yellow Apricorn"
            if "é" in name:
                name = name.replace("é", "e")
            if "TM" in name or "HM" in name:
                name = ""
            description = item.contents[counter].contents[5].contents[0]
            type = item.contents[counter].contents[3].contents[0].title()
            lowername = name.lower()
            items[lowername] = Item(name, description, type)
            counter += 2
        except IndexError:
            break

def load_moves():
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/List_of_moves")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    move = soup.find('table', class_='sortable roundy').contents[1].contents[1].contents[1]
    counter = 3
    while True:
        try:
            name = move.contents[counter].contents[3].contents[0].contents[0]
            if name.lower() in ["breakneck blitz", "all-out pummeling", "supersonic skystrike",
                                "acid downpour", "tectonic rage", "continental crush", "savage spin-out",
                                "never-ending nightmare", "corkscrew crash", "inferno overdrive",
                                "hydro vortex", "bloom doom", "gigavolt havoc", "shattered psyche",
                                "subzero slammer", "devastating drake", "black hole eclipse", "twinkle tackle"]: # Z-Moves
                cat = "Physical or Special"
            else:
                cat = move.contents[counter].contents[7].contents[0].contents[0].contents[0]
            if not name.lower() in movelist:
                movelist.append(name.lower())
                type = move.contents[counter].contents[5].contents[0].contents[0].contents[0]
                bp = move.contents[counter].contents[13].contents[0].rstrip("\n")
                lowername = name.lower()
                zp = get_Z_Power(bp, lowername)
                pp = move.contents[counter].contents[11].contents[0].rstrip("\n")
                acc = move.contents[counter].contents[15].contents[0].rstrip("\n")
                acc = acc.replace("%", "")
                if acc == "—":
                    acc = "Never Miss"
                if name in ["Guillotine", "Horn Drill", "Fissure", "Sheer Cold"]:
                    bp = "OHKO"
                    acc = "(Level of user - Level of target) - 30"
                if name in ["Protect", "Detect", "Quick Guard", "Wide Guard", "King's Shield", "Spiky Shield",
                            "Baneful Bunker", "Crafty Shield"]:
                    acc = "—"
                moves[lowername] = Move(name, type, cat, bp, zp, pp, acc, "", "", "")
            counter += 2
        except IndexError:
            break
        except TypeError:
            if name == "Sonic Boom":
                bp = "Fixed 20 Damage"
            elif name == "Dragon Rage":
                bp = "Fixed 40 Damage"
            pp = move.contents[counter].contents[11].contents[0].rstrip("\n")
            acc = move.contents[counter].contents[15].contents[0].rstrip("\n")
            acc = acc.replace("%", "")
            lowername = name.lower()
            zp = get_Z_Power(bp, lowername)
            moves[lowername] = Move(name, type, cat, bp, zp, pp, acc, "", "", "")
            counter += 2
            continue
    getDescriptions()
    get_Z_Moves()
    get_TM()

def get_Z_Power(bp, lowername):
    zp = ''
    try:
        newbp = int(bp)
        if newbp <= 55:
            zp = "100"
        elif newbp <= 65 and newbp >= 60:
            zp = "120"
        elif newbp <= 75 and newbp >= 70:
            zp = "140"
        elif newbp <= 85 and newbp >= 80:
            zp = "160"
        elif newbp <= 95 and newbp >= 90:
            zp = "175"
        elif newbp == 100:
            zp = "180"
        elif newbp == 110:
            zp = "185"
        elif newbp <= 125 and newbp >= 120:
            zp = "190"
        elif newbp == 130:
            zp = "195"
        elif newbp > 140:
            zp = "200"
        if lowername == "flying press":
            zp = "170"
        elif lowername == "core enforcer":
            zp = "140"
        elif lowername == "v-create":
            zp = "220"
        elif lowername in ["hex", "weather ball"]:
            zp = "160"
        elif lowername == "mega drain":
            zp = "120"
        elif lowername == "gear grind":
            zp = "180"
    except ValueError:
        zp = ''
    return zp

def getDescriptions():
    """
    Gets the descriptions for the moves.
    :return: None
    """
    r  = requests.get("http://pokemondb.net/move/all")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    move = soup.find('table', class_='data-table wide-table').contents[3]
    counter = 1
    for thing in sorted(movelist):
        try:
            moves[thing].description = move.contents[counter].contents[13].contents[0]
            counter += 2
        except IndexError:
            counter += 2
            pass

def get_Z_Moves():
    """
    Gets the Z-Status move descriptions and applies them to the class already created.
    :return: None
    """
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/Z-Move")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    move = soup.find_all('table', class_='sortable roundy')[4].contents[1].contents[1].contents[1]
    counter = 3
    while True:
        try:
            name = move.contents[counter].contents[1].contents[1].contents[0].contents[0]
            description = move.contents[counter].contents[7].contents[0].rstrip("\n")[1:]
            name = name.lower()
            moves[name].zDesc = description
            counter += 2
        except IndexError:
            break
def get_TM():
    """
    Get a list of TM numbers and apply them to the move class already created.
    :return: None
    """
    r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/TM")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    move = soup.find_all('table', class_='sortable')[6]
    counter = 3
    while True:
        try:
            number = move.contents[counter].contents[1].contents[1].contents[0]
            name = move.contents[counter].contents[3].contents[1].contents[0]
            moves[name.lower()].tm = number
            newnumber = int(number[0])
            if newnumber == 0:
                newnumber = int(number[1])
            else:
                newnumber = int(number)
            tm[newnumber] = moves[name.lower()]
            counter += 2
        except IndexError:
            break

if __name__ == "__main__":
    load_mons()
    load_abilities()
    load_items()
    load_moves()


