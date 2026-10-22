#!/usr/bin/env python3
"""
Activity 3: RPG Character Forge (STARTER)

TODOs 1-4 (the Character class)
TODOs 5-6 (save/load)

Run the file often to test as you go:
    python code/character_forge_starter.py
"""

SAVE_FILE = "character_save.txt"


class Character:
    def __init__(self, name, hp, level):
        # TODO 1: Set self.name, self.hp, self.max_hp (same as starting hp),
        # self.level, and self.inventory (start as an empty list).
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.level = level
        self.inventory = []

        # Journal Entry TODO 1: Replaced pass with assignments that
        # store the character's starting information as attributes.
        # self refers to the specific Character object being initialized.
        # self.hp stores current health, while self.max_hp stores
        # the starting health value used when restoring health.
        # self.level stores the character's starting level.
        # self.inventory creates a separate empty list for each character.

    def take_damage(self, amount):
        # TODO 2: Reduce self.hp by `amount`. Don't let it go below 0.
        # Check: Reject negative damage because subtracting a negative
        # number would increase health instead of reducing it.
        if amount < 0:
            print("Damage cannot be negative.")
            return

        # Check discussed in class: Calculate the remaining health first.
        # Use self.hp to access this character's current health.
        # If the result is negative, store 0; otherwise, store the result.
        new_hp = self.hp - amount

        if new_hp < 0:
            self.hp = 0
        else:
            self.hp = new_hp

        # Journal Entry TODO 2: Used a temporary variable named new_hp
        # to check the result before updating the character's health.
        # Corrected hp and self_hp from my notes to self.hp.
        # This updates the object's attribute and keeps health at or above 0.
        # self.max_hp stays unchanged.

    def level_up(self):
        # TODO 3: Increase self.level by 1 and restore self.hp to self.max_hp.
        self.level += 1
        self.hp = self.max_hp
        
        # Journal Entry TODO 3: Used += to increase the level by 1.
        # Assigned self.max_hp to self.hp to restore full health.
        # This uses the maximum health stored when the object was created,
        # so the method works with different starting health values.

    def display_stats(self):
        # TODO 4: Print name, hp/max_hp, level, and inventory.
        print(f"Name: {self.name}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Level: {self.level}")
        print(f"Inventory: {self.inventory}")
        print()

        # Journal Entry TODO 4: Used f-strings to display the character's
        # name, health, level, and inventory from its attributes.
        # Displayed self.hp and self.max_hp together to show current
        # health compared with maximum health.
        # Printed the inventory list, which displays [] when empty.
        # Added print() to leave a blank line after the stats.

    def save_to_file(self, filename):
        # TODO 5: Open `filename` for writing and write self.name, self.hp,
        # and self.level (e.g. one value per line). Use `with open(...)`.
        with open(filename, "w") as file:
            file.write(f"{self.name}\n")
            file.write(f"{self.hp}\n")
            file.write(f"{self.level}\n")


        # Journal Entry TODO 5: Used with open(filename, "w") to open
        # the save file for writing. This creates the file if needed
        # or replaces its previous contents if it already exists.
        # Used file.write() and f-strings to write each value as text.
        # Added \n after each value so it appears on a separate line.
        # The with statement automatically closes the file afterward.

def load_character(filename):
    """Load a saved character from filename, or return None if not found."""

    # TODO 6: Open `filename` for reading inside a try/except FileNotFoundError
    # block. Read back name, hp, and level, and return a new Character built
    # from those values. Return None if the file doesn't exist yet.
    try:
        with open(filename, "r") as file:
            name = file.readline().strip()
            hp = int(file.readline().strip())
            level = int(file.readline().strip())

        return Character(name, hp, level)
    except FileNotFoundError:
        return None
    except ValueError:
        print("The save file contains missing or invalid numeric data.")
        return None
    except OSError:
        print("The save file could not be read.")
        return None

    # Journal Entry TODO 6: Opened the save file in reading mode.
    # Used readline() to read name, hp, and level in their saved order.
    # Used strip() to remove the newline and surrounding whitespace.
    # Converted hp and level to integers because files store these as text.
    # Returned a new Character object using the loaded values.
    # Used except FileNotFoundError to return None if no save file exists,
    # allowing main() to create a new character.

    # Additional checks: Kept FileNotFoundError for a missing save file.
    # Added ValueError for missing or noninteger HP and level values.
    # Added OSError for other file-reading problems, such as denied access.
    # Returning None allows main() to create a new character.

def main():
    print("=== RPG Character Forge ===\n")

    hero = load_character(SAVE_FILE)

    if hero is None:
        print("No saved character found. Creating a new one!")
        hero = Character("Hero", 100, 1)

    hero.display_stats()

    hero.take_damage(30)
    hero.level_up()
    hero.display_stats()

    hero.save_to_file(SAVE_FILE)
    print(f"\nSaved to {SAVE_FILE}.")


if __name__ == "__main__":
    main()