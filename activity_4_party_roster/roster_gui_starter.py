#!/usr/bin/env python3
"""
Activity 4, Week 9: Party Roster Manager - GUI (STARTER)

The database functions below are already complete (from Week 8) so you can
focus on the GUI. Follow the numbered TODOs in order. Run the file often:
    python code/roster_gui_starter.py
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_FILE = "roster.db"


# --- Database layer (already complete - reused from Week 8) ---

def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hp INTEGER NOT NULL,
            level INTEGER NOT NULL,
            char_class TEXT NOT NULL
        )
        """
    )
    conn.commit()


def add_character(conn, name, hp, level, char_class):
    conn.execute(
        "INSERT INTO characters (name, hp, level, char_class) VALUES (?, ?, ?, ?)",
        (name, hp, level, char_class),
    )
    conn.commit()


def list_characters(conn):
    cursor = conn.execute("SELECT id, name, hp, level, char_class FROM characters")
    return cursor.fetchall()


def delete_character(conn, character_id):
    cursor = conn.execute("DELETE FROM characters WHERE id = ?", (character_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- GUI layer (build this part) ---

class RosterApp:
    def __init__(self, root, conn):
        self.conn = conn
        root.title("Party Roster Manager")

        form_frame = tk.Frame(root)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        # TODO 1: Add labeled Entry widgets for name, hp, level, and class
        # using .grid(row=..., column=...) inside form_frame. Save each Entry
        # widget as self.name_entry, self.hp_entry, self.level_entry,
        # self.class_entry so the other methods can read from them.
        tk.Label(form_frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="HP").grid(row=1, column=0, sticky="w")
        self.hp_entry = tk.Entry(form_frame)
        self.hp_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Level").grid(row=2, column=0, sticky="w")
        self.level_entry = tk.Entry(form_frame)
        self.level_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Class").grid(row=3, column=0, sticky="w")
        self.class_entry = tk.Entry(form_frame)
        self.class_entry.grid(row=3, column=1)

        add_button = tk.Button(form_frame, text="Add Character", command=self.on_add_click)
        add_button.grid(row=4, column=0, columnspan=2, pady=5)

        delete_button = tk.Button(root, text="Delete Selected", command=self.on_delete_click)
        delete_button.grid(row=2, column=0, pady=5)

        columns = ("id", "name", "hp", "level", "class")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
        self.tree.grid(row=1, column=0, padx=10, pady=10)

        self.refresh_list()

    def on_add_click(self):
        # TODO 2: Read the four entries. Reject blank name/class fields and
        # non-integer or nonpositive HP/level with messagebox.showerror.
        # Otherwise call add_character(...), clear the entries (e.g.
        # entry.delete(0, tk.END)), and call self.refresh_list().
                # Read the text from the four input boxes.
        name = self.name_entry.get().strip()
        char_class = self.class_entry.get().strip()
        hp_text = self.hp_entry.get()
        level_text = self.level_entry.get()

        # Reject blank names and classes before continuing.
        if not name or not char_class:
            messagebox.showerror(
                "Invalid Input",
                "Name and class cannot be blank."
            )
            return

        # Convert HP and level from text to integers.
        try:
            hp = int(hp_text)
            level = int(level_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "HP and level must be whole numbers."
            )
            return

        # Successful conversion does not guarantee a positive value.
        if hp < 1 or level < 1:
            messagebox.showerror(
                "Invalid Input",
                "HP and level must be at least 1."
            )
            return

        # Save the character only after all checks pass.
        add_character(self.conn, name, hp, level, char_class)

        # Clear the fields after the character has been added.
        self.name_entry.delete(0, tk.END)
        self.hp_entry.delete(0, tk.END)
        self.level_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)

        self.refresh_list()

    def refresh_list(self):
        # TODO 3: Loop over self.tree.get_children() and delete each displayed
        # row. Then loop over list_characters(self.conn) and add each row with
        # self.tree.insert("", tk.END, values=row).
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in list_characters(self.conn):
            self.tree.insert("", tk.END, values=row)

    def on_delete_click(self):
        # TODO 4: If nothing is selected, show an informational message.
        # Otherwise get the selected Treeview item's id, call
        # delete_character(...), then refresh_list().
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "No Selection",
                "Please select a character to delete."
            )
            return

        values = self.tree.item(selected[0], "values")
        character_id = int(values[0])

        delete_character(self.conn, character_id)
        self.refresh_list()


def main():
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)

    root = tk.Tk()
    RosterApp(root, conn)
    root.mainloop()

    conn.close()


if __name__ == "__main__":
    main()
