#!/usr/bin/env python3
"""
Activity 4, Week 8: Party Roster Manager - Database (STARTER)

Follow the numbered TODOs in order. Run the file often to test as you go:
    python code/roster_db_starter.py
"""

import sqlite3

DB_FILE = "roster.db"


def init_db(conn):
    """Create the characters table if it doesn't already exist."""

    # TODO 1: Run CREATE TABLE IF NOT EXISTS with an auto-generated integer id
    # and required name (TEXT), hp (INTEGER), level (INTEGER), and
    # char_class (TEXT) columns. Then conn.commit().
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hp INTEGER NOT NULL,
            level INTEGER NOT NULL,
            char_class TEXT NOT NULL
        )
    """)
    conn.commit()


def add_character(conn, name, hp, level, char_class):
    """Insert a new character row."""

    # TODO 2: Use a parameterized INSERT (with ? placeholders) to add a row.
    # Never use an f-string to put `name`/`char_class` directly into the SQL.
    # Don't forget conn.commit().
    conn.execute("""
        INSERT INTO characters (name, hp, level, char_class)
        VALUES (?, ?, ?, ?)
    """, (name, hp, level, char_class))
    conn.commit()


def list_characters(conn):
    """Return all character rows as a list of tuples."""

    # TODO 3: Run a SELECT statement and return cursor.fetchall().
    cursor = conn.execute("SELECT * FROM characters")
    rows = cursor.fetchall()
    return rows


def delete_character(conn, character_id):
    """Delete a character row by id."""

    # TODO 4: Use a parameterized DELETE (with a ? placeholder for the id).
    # Commit, then return True if a row was deleted or False if the ID was
    # not found.
    cursor = conn.execute("DELETE FROM characters WHERE id = ?", (character_id,))
    conn.commit()
    return cursor.rowcount > 0


def print_roster(rows):
    if not rows:
        print("(roster is empty)")
        return
    for row in rows:
        char_id, name, hp, level, char_class = row
        print(f"  [{char_id}] {name} - {char_class}, Level {level}, HP {hp}")


def main():
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)

    # TODO 5: Finish this menu loop. Validate nonblank name/class and
    # positive integer HP, level, and delete ID inputs. Handle non-integer
    # values with a helpful message and return to the menu without crashing.
    # Call the matching function and report when a delete ID is not found.
    while True:
        print("\n=== Party Roster Manager (Database) ===")
        print("1) Add character")
        print("2) List roster")
        print("3) Delete character")
        print("4) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            char_class = input("Class: ").strip()

            if not name or not char_class:
                print("Name and class cannot be blank.")
                continue

            try:
                hp = int(input("HP: "))
                level = int(input("Level: "))
            except ValueError:
                print("HP and level must be whole numbers.")
                continue

            if hp <= 0 or level <= 0:
                print("HP and level must be greater than 0.")
                continue

            add_character(conn, name, hp, level, char_class)
            print(f"{name} was added.")

        elif choice == "2":
            rows = list_characters(conn)
            print_roster(rows)

        elif choice == "3":
            try:
                character_id = int(input("ID to delete: "))
            except ValueError:
                print("The character ID must be a whole number.")
                continue

            if character_id <= 0:
                print("The character ID must be greater than 0.")
                continue

            if delete_character(conn, character_id):
                print("Character deleted.")
            else:
                print("No character was found with that ID.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Please enter 1, 2, 3, or 4.")

    conn.close()


if __name__ == "__main__":
    main()
