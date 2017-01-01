"""
Create dictionaries to map abilities to pokemon, and vice versa.
"""
from loaddex import *

rotom_forms = ["Wash", "Heat", "Mow", "Fan", "Frost"]
non_changing = ["Incarnate", "Standard", "Altered", "Land Forme", "Normal Forme", "Aria Forme", "Solo", "50%", "Male",
                "Female", "Sunny", "Rainy", "Snowy", "Meteor", "Baile", "Pom-Pom", "Pa'u", "Sensu", "Cosplay",
                "East", "West", "Style", "Overcast", "Sunshine", "Spiky-eared", "Red-Striped", "Blue-Striped", "Eternal"]
other_forms = ["Midday", "Midnight", "Small", "Average", "Large", "Super", "Cloak"]
keep_alt = ["Mega", "Ash-Greninja", "Kyurem", "Primal"]
ability_to_mons = {}
mon_to_abilities = {}

def ability_to_mon():
    """
    Maps abilities to Pokemon, and vice versa.
    :return:
    """

    for name in names:
        name = name.lower()
        mon_to_abilities[name] = []
    for ability in abilities.values():
        url = ability.name.title()
        url = url.replace (" ", "_")
        r  = requests.get("http://bulbapedia.bulbagarden.net/wiki/"+url+"_(Ability)")
        ability_name = ability.name.lower()
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        mon = soup.find_all('table', class_='roundy')
        counter = 3
        ability_to_mons[ability_name] = []
        while True:
            try:
                if ability.name in ["Turboblaze", "Teravolt", "Bulletproof", "Skill Link", "Mega Launcher",
                                    "Soundproof", "Dancer", "Liquid Ooze", "Reckless", "Rock Head", "Mold Breaker",
                                    "Iron Fist"]:
                    try:
                        name = mon[7].contents[counter].contents[3].contents[1].contents[0].contents[0]
                        altname = mon[7].contents[counter].contents[3].contents[3].contents[0].contents[0].contents[0] # Alt Form
                        fullname = name + " " + altname
                        if "Alola" in fullname:
                            fullname = "Alolan " + name
                        elif "Mega Charizard X" in fullname:
                            fullname = "Mega Charizard X"
                        elif "Mega Charizard Y" in fullname:
                            fullname = "Mega Charizard Y"
                        elif "Mega Mewtwo X" in fullname:
                            fullname = "Mega Mewtwo X"
                        elif "Mega Mewtwo Y" in fullname:
                            fullname = "Mega Mewtwo Y"
                        elif "Attack" in fullname:
                            fullname = "Deoxys Attack"
                        elif "Defense" in fullname:
                            fullname = "Deoxys Defense"
                        elif "Speed" in fullname:
                            fullname = "Deoxys Speed"
                        elif "Therian" in fullname:
                            fullname = name + " " + "Therian"
                        elif "Origin" in fullname:
                            fullname = "Giratina Origin"
                        elif "Sky Forme" in fullname:
                            fullname = "Shaymin Sky"
                        elif "Zen Mode" in fullname:
                            fullname = "Darmanitan Zen"
                        elif "Pirouette" in fullname:
                            fullname = "Meloetta Pirouette"
                        elif "Shield" in fullname:
                            name = "Aegislash Shield"
                        elif "Blade" in fullname:
                            name = "Aegislash Blade"
                        elif "School" in fullname:
                            fullname = "Wishiwashi School"
                        elif "Core" in fullname:
                            fullname = "Minior Core"
                        for item in keep_alt:
                            if item in fullname:
                                fullname = altname
                        for item in rotom_forms:
                            if item in fullname:
                                altname = altname.split()
                                fullname = "Rotom " + altname[0]
                        for item in other_forms:
                            if item in fullname:
                                altname = altname.split()
                                fullname = name + " " + altname[0]
                        for item in non_changing:
                            if item in fullname:
                                fullname = name
                        name = fullname.lower()
                    except IndexError:
                        try:
                            name = mon[7].contents[counter].contents[3].contents[1].contents[0].contents[0]
                            fullname = name.lower()
                        except IndexError:
                            break

                    name = fullname.lower()
                elif ability.name in ["Sheer Force", "Serene Grace"]:
                    try:
                        altname = mon[8].contents[counter].contents[3].contents[3].contents[0].contents[0].contents[0] # Alt Form
                        fullname = name + " " + altname
                        if "Mega" in fullname:
                            fullname = "Mega " + name
                        elif "Sky Forme" in fullname:
                            fullname = "Shaymin Sky"
                        elif "Pirouette" in fullname:
                            fullname = "Meloetta Pirouette"
                        elif "Aria Forme" in fullname:
                            fullname = name
                        for item in non_changing:
                            if item in fullname:
                                fullname = name
                    except IndexError:
                        try:
                            name = mon[8].contents[counter].contents[3].contents[1].contents[0].contents[0]
                            fullname = name
                        except IndexError:
                            break
                    name = fullname.lower()
                elif ability.name in ["Pickup"]:
                    try:
                        altname = mon[17].contents[counter].contents[3].contents[3].contents[0].contents[0].contents[0] # Alt Form
                        fullname = name + " " + altname
                        if "Alola" in fullname:
                            fullname = "Alolan " + name
                        for item in other_forms:
                            if item in fullname:
                                altname = altname.split()
                                fullname = name + " " + altname[0]
                    except IndexError:
                        try:
                            name = mon[17].contents[counter].contents[3].contents[1].contents[0].contents[0]
                            fullname = name
                        except IndexError:
                            break
                    name = fullname.lower()
                else:
                    try:
                        name = mon[6].contents[counter].contents[3].contents[1].contents[0].contents[0]
                        altname = mon[6].contents[counter].contents[3].contents[3].contents[0].contents[0].contents[0] # Alt Form
                        fullname = name + " " + altname
                        if "Alola" in fullname:
                            fullname = "Alolan " + name
                        elif "Mega Charizard X" in fullname:
                            fullname = "Mega Charizard X"
                        elif "Mega Charizard Y" in fullname:
                            fullname = "Mega Charizard Y"
                        elif "Mega Mewtwo X" in fullname:
                            fullname = "Mega Mewtwo X"
                        elif "Mega Mewtwo Y" in fullname:
                            fullname = "Mega Mewtwo Y"
                        elif "Attack" in fullname:
                            fullname = "Deoxys Attack"
                        elif "Defense" in fullname:
                            fullname = "Deoxys Defense"
                        elif "Speed" in fullname:
                            fullname = "Deoxys Speed"
                        elif "Therian" in fullname:
                            fullname = name + " " + "Therian"
                        elif "Origin" in fullname:
                            fullname = "Giratina Origin"
                        elif "Shield" in fullname:
                            fullname = "Aegislash Shield"
                        elif "Blade" in fullname:
                            fullname = "Aegislash Blade"
                        elif "Sky Forme" in fullname:
                            fullname = "Shaymin Sky"
                        elif "Zen Mode" in fullname:
                            fullname = "Darmanitan Zen"
                        elif "Pirouette" in fullname:
                            fullname = "Meloetta Pirouette"
                        elif "School" in fullname:
                            fullname = "Wishiwashi School"
                        elif "Core" in fullname:
                            fullname = "Minior Core"
                        elif "10%" in fullname:
                            altname = altname.split()
                            fullname = name + " " + altname[0]
                        elif "Complete" in fullname:
                            altname = altname.split()
                            fullname = name + " " + altname[0]
                        for item in keep_alt:
                            if item in fullname:
                                fullname = altname
                        for item in rotom_forms:
                            if item in fullname:
                                altname = altname.split()
                                fullname = "Rotom " + altname[0]
                        for item in other_forms:
                            if item in fullname:
                                if "Burmy" in fullname:
                                    pass
                                else:
                                    altname = altname.split()
                                    fullname = name + " " + altname[0]
                        for item in non_changing:
                            if item in fullname:
                                fullname = name
                        if "Burmy" in fullname:
                            fullname = "Burmy"
                        name = fullname.lower()
                    except IndexError:
                        try:
                            name = mon[6].contents[counter].contents[3].contents[1].contents[0].contents[0]
                            fullname = name.lower()
                        except IndexError:
                            break
                    name = fullname.lower()
                if "nidoran♀" in name:
                    name = "nidoran f"
                if "nidoran♂" in name:
                    name = "nidoran m"


                try:
                    if name not in ability_to_mons[ability_name]:
                        ability_to_mons[ability_name].append(name)
                    if name == "pumpkaboo":
                        mon_to_abilities["pumpkaboo small"].append(ability_name)
                        mon_to_abilities["pumpkaboo average"].append(ability_name)
                        mon_to_abilities["pumpkaboo large"].append(ability_name)
                        mon_to_abilities["pumpkaboo super"].append(ability_name)
                    elif name == "gourgeist":
                        mon_to_abilities["gourgeist small"].append(ability_name)
                        mon_to_abilities["gourgeist average"].append(ability_name)
                        mon_to_abilities["gourgeist large"].append(ability_name)
                        mon_to_abilities["gourgeist super"].append(ability_name)
                    else:
                        if ability_name not in mon_to_abilities[name]:
                            mon_to_abilities[name].append(ability_name)
                    counter += 2
                except KeyError:
                    print(fullname)
                    counter += 2
            except IndexError:
                break
            except AttributeError:
                print(ability.name)
                continue


