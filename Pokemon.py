"""
Provides a class for information about the Pokemon.
"""

class Pokemon():
    """
    Uses a Pokemon's data to construct a class.
    """

    def __init__(self, number, name, hp, attack, defense, spattack, spdefense, speed):
        """
        args:
            str number: National Dex number of the Pokemon, can be 1.a for a mega
            str name: Name of the Pokemon
            int attack: Attack stat
            int defense: Defense stat
            int spattack: Special Attack stat
            int spdefense: Special Defense stat
            int speed: Speed stat
        """
        self.number=number
        self.name=name
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.spattack=spattack
        self.spdefense=spdefense
        self.speed=speed

    def __str__(self):
        """
        Return a string representation of the Pokemon.
        """
        return (str(self.number) + ": " +
            self.name.title() + "\n" + "HP: " + "{:16d}".format(self.hp) + "\n" +
                "Attack: " + "{:12d}".format(self.attack) + "\n" +
                "Defense: " + "{:11d}".format(self.defense) + "\n" +
                "Special Attack: " + "{:4d}".format(self.spattack) + "\n" +
                "Special Defense: " + "{:3d}".format(self.spdefense) + "\n" +
                "Speed: " + "{:13d}".format(self.speed))

    __repr__ = __str__

class Ability():
    """
    Uses an ability's data to construct a class.
    """
    def __init__(self, name, description, generation):
        """
        args:
            str name: Name of ability.
            str description: Description of ability.
            str generation: Generation the ability debuted in. (Unused)
        """
        self.name = name
        self.description = description
        self.generation = generation

    def __str__(self):
        """
        Return a string representation of the Ability.
        """
        return (self.name + ": " + self.description)

    __repr__ = __str__

class Item():
    """
    Uses an Item's data to construct a class.
    """
    def __init__(self, name, description, type):
        """
        args:
            str name: Name of the item.
            str description: Description of the item.
            str type: Category item is in. (Unused)
        """
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        """
        Return a string representation of the Item.
        """
        return (self.name + ": " + self.description)

    __repr__ = __str__


class Move():
    """
    Uses a move's data to construct a class.
    """
    def __init__(self, name, type, cat, bp, zp, pp, acc, description, zDesc, tm):
        """
        args:
            str name: Name of move.
            str type: Type of move.
            str cat: Category of move (Physical or Special).
            str bp: Base Power, can be —.
            str zp: Z-Move power
            str pp: Power Points.
            str acc: Accuracy, can be —.
            str description: Description of move, along with an effects.
            str zDesc: Description of Z-Move.
            str tm: TM Number
        """
        self.name = name
        self.type = type
        self.cat = cat
        self.bp = bp
        self.zp = zp
        self.pp = pp
        self.acc = acc
        self.description = description
        self.zDesc = zDesc
        self.tm = tm

    def __str__(self):
        """
        Return a string representation of the Move.
        """
        string = (self.name + ": \nType: " + self.type + "\nCategory: " + self.cat
               + "\nBase Power: " + "  " + self.bp)
        if not self.zp == "":
            string += "\nZ-Base Power: " + self.zp
        string += ("\nPower Points: "
               + "{:2d}".format(int(self.pp)) + "\nAccuracy: " + "    " + self.acc + "\nDescription: " + self.description)
        if not self.zDesc == "" or self.zDesc == "None":
            string += "\nZ-Move: " + self.zDesc + "."
        if not self.tm == "":
            string += "\nTM: " + self.tm
        return(string)

    __repr__ = __str__