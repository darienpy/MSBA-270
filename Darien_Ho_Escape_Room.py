def room_one(inventory):
    """Room 1: the player arrives here first."""

     # TODO 1: Print a short description of the starting room.
        # Example: "You wake up in a dusty library. There is a door to the LEFT
        # and a large cabinet in front of you."
    if has_item(inventory, "sledgehammer"):
        print("You're still in the same room, what do you do?")
    else:
        print("You wake up in a dusty library. There is a door to the LEFT and a large cabinet in front of you.")
    choice = input("What do you do? ").lower()

    # TODO 3: Write if/elif/else branches for this room's choices.
    # - one branch should print(...) and return "room_two"
    # - one branch should search the cabinet, maybe add an item to inventory,
    #   and return "room_one" again (stay in this room)
    # - an else branch should give a hint and return "room_one" again

    if choice == "go left":
        print("You go through the door and end up in a hollow, dark room.")
        return "room_two"
    elif choice == "search cabinet" or choice == "search desk":
        if has_item(inventory, "sledgehammer"):
            print("You already found the sledgehammer.")
        else:
            print("You found a sledgehammer!")
            inventory.append("sledgehammer")
    else:
        print('Have you tried to "go left" or "search cabinet"?')
        return "room_one"

    # TODO 4: replace this placeholder return once your branches are written
    return "room_one"

def room_two(inventory):
    """Room 2: Enter upon leaving room one."""

    print("You are in room two. There is a door ahead blocked by wooden planks.")

    choice = input("What do you do? ").lower()

    if choice == "go back":
        print("You return to the library.")
        return "room_one"

    elif choice == "use sledgehammer":
        for item in inventory:
            if item == "sledgehammer":
                print("You smash through the planks and escape!")
                return "escaped"

        print("You need a tool to break through the planks.")
        return "room_two"

    elif choice == "quit":
        return "quit"

    else:
        print('Try "go back", "use sledgehammer", or "quit".')
        
        return "room_two"


def has_item(inventory, item_name):
    """Return True if item_name is in the player's inventory."""

    # TODO 6: Use a for loop to check each item in 'inventory'.
    # If it matches item_name, return True. If the loop finishes without
    # finding it, return False.
    for item in inventory:
        if item == item_name:
            return True

    return False



def main():
    print("=== Escape Room ===")
    print("Type 'quit' at any time to give up.\n")
    inventory = []
    current_room = "room_one"

    # TODO 2: Set the loop condition so the game keeps running until the
    # player escapes or quits. Hint: use a `playing` boolean flag.
    playing = True
    while playing:
        if current_room == "room_one":
            current_room = room_one(inventory)
        elif current_room == "room_two":
            current_room = room_two(inventory)
        elif current_room == "escaped":
            print("\nYou escaped! Congratulations!")
            playing = False
        elif current_room == "quit":
            print("\nMaybe next time!")
            playing = False

if __name__ == "__main__":
    main()
