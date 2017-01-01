# PythonDex  v0.5.5

## Credits
- - - -
Tools used:
[Python Requests](http://docs.python-requests.org/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for text processing.
[Bulbapedia](http://bulbapedia.bulbagarden.net), [Serebii](http://serebii.net), and [Pokemon Database](http://pokemondb.net/) for information.

Author: Scott C. ([swc19](https://github.com/swc19))

## Usage
- - - -
1. Assuming installation of Python 3.5, the first step is to clone this repo.

    ```
    $ git clone https://github.com/swc19/pythondex.git
    ```
2. BS4 and Requests are also required to be installed.
    ```
    $ pip install requests
    $ pip install beautifulsoup4
    ```
*  The main program, `get-mons.py`, serves as a hub to get between different modules of the Dex. Possible abilities are the option to
   search for a Pokémon, Move, Ability, or Item.

    ```
    300: Skitty
    HP:               50
    Attack:           45
    Defense:          45
    Special Attack:   35
    Special Defense:  35
    Speed:            50
    This Pokemon's possible abilities are: Wonder Skin, Cute Charm, Normalize

    Enter ability (Leave blank to exit): Shields Down
    Shields Down: When its HP becomes half or less, the Pokémon's shell breaks and it becomes aggressive.
    Pokemon with Shields Down: Minior

    Enter Move: (Leave blank to exit): Earthquake
    Earthquake:
    Type: Ground
    Category: Physical
    Base Power:   100
    Power Points: 10
    Accuracy:     100
    Description: Power is doubled if opponent is underground from using Dig.

    Enter Item: (Leave blank to exit): Master Ball
    Master Ball: The best Ball with the ultimate level of performance.
                 It will catch any wild Pokémon without fail.
    ```
* A catching simulator is also included. The user will be prompted to enter a wild Pokémon, its level, percent of HP remaining,
    the ball used, and if it has a status ailment. The program will then simulate a capture of the Pokémon, and return
    whether it was caught or missed, along with a catch chance.

    ```
    Pokemon: Metapod
    Level: 10
    Percent of HP remaining? (Enter 0 for 1hp) 0
    Type of ball: Net
    (F)reeze, (S)leep, (P)aralyze, or (N)one? P
    Shake...
    Shake...
    Shake...
    Caught!
    Catch rate: 95.56%
    ```

## Things to Note
-  - - -
* Pokemon with alternate Formes, such as Deoxys, Zygarde, or any Mega will have a .a, .b, or .c appended to its Pokédex number.

    ```
    774: Minior
    HP:                60
    Attack:            60
    Defense:          100
    Special Attack:    60
    Special Defense:  100
    Speed:             60
    This Pokemon's possible abilities are: Shields Down

    774.a: Minior Core
    HP:                60
    Attack:           100
    Defense:           60
    Special Attack:   100
    Special Defense:   60
    Speed:            120
    This Pokemon's possible abilities are: Shields Down
    ```

* Special designations for alternate forms include the following:

    ```
    Mega [Pokemon]
    Alolan [Pokemon]
    Deoxys [Attack, Defense, or Speed]
    Shaymin Sky
    Rotom [Wash, Heat, Frost, Mow, Fan]
    Giratina Origin
    Darmanitan Zen
    [Tornadus, Thundurus, Landorus] Therian
    Meloetta Pirouette
    Aegislash [Shield, Blade]
    Pumpkaboo/Gourgeist [Small, Average, Large, Super]
    Zygarde [10%, Complete]
    Lycanroc [Midday, Midnight]
    Wishiwashi School
    ```

## Planned Features
- - - -
* [ ] Optimize loading times to < 10 seconds. (Currently 70-90 seconds)
* [x] Have searchable lists for Abilities, Items, TM's, and Moves.
* [x] Convert \[Pokémon] \(Mega Pokémon) to Mega [Pokémon].
* [x] Add designation in abilities for Megas (if possible).
* [x] "Catching Simulator": Select ball, Pokémon to catch, Status, etc.
        Will use newest formula, and give an estimated probability with the "shake test" formula.
        Will have to take into consideration certain types of Poké Balls.