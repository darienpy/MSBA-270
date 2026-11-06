# Party Roster Manager

**Activity 4 — Week 8 Database and Week 9 GUI**

## Project purpose

This project manages a roster of fictional RPG characters using a SQLite database. It includes a terminal menu and a Tkinter graphical interface. Both versions can add characters, display the roster, and delete characters by database ID. Committed changes remain available after the program closes.

Repository: [darienpy/MSBA-270](https://github.com/darienpy/MSBA-270)

## Python and dependencies

The project uses **Python 3** and only standard-library modules: `sqlite3`, `tkinter`, and Tkinter's `ttk` and `messagebox`. The source uses f-strings, which require Python 3.6 or later. Check the exact version of your selected interpreter with:

```bash
python3 --version
```

No third-party Python packages or `requirements.txt` are needed. The GUI requires a Python installation with Tkinter support and a graphical desktop. To check Tkinter, run:

```bash
python3 -m tkinter
```

A small demonstration window should open. If Tkinter is unavailable, use a Python installation that includes Tcl/Tk support; it is not a project-specific pip dependency.

## Project files

Place this README in the activity folder, with both Python files in its `code` subfolder:

| File | Purpose |
| --- | --- |
| `README.md` | Setup, usage, skills, limitations, and credits. |
| `code/roster_db_starter.py` | Completed terminal version with a menu and input validation. |
| `code/roster_gui_starter.py` | Completed GUI version with input fields, a roster table, and add/delete buttons. |

The filenames retain `starter` from the course materials, but the numbered TODOs in these two files are implemented. No sample database is required.

## How to run

Open a terminal in the `activity_4_party_roster` folder containing this README and the `code` subfolder.

Run the terminal version:

```bash
python3 code/roster_db_starter.py
```

Run the GUI version:

```bash
python3 code/roster_gui_starter.py
```

On Windows, use `py` in place of `python3` if that is your Python launcher. If the Python files are directly beside this README instead of inside `code`, omit `code/` from the commands.

Both programs create `roster.db` and the `characters` table automatically when needed. Run them from the same writable activity folder to use the same local database. Close the terminal version before switching to the GUI for the example below.

## Completed features and example

- Add a character with a name, class, positive integer HP, and positive integer level.
- List saved characters with automatically generated database IDs.
- Delete by typed ID in the terminal or by selected row in the GUI.
- Reject blank names/classes, noninteger HP/level, and nonpositive HP/level.
- In the terminal, reject invalid deletion IDs and report when an ID does not exist.
- In the GUI, show an informational message when no row is selected for deletion. Invalid add attempts retain the entered text for correction; successful additions clear the fields and refresh the table.

For example, choose **1) Add character** in the terminal and enter:

```text
Name: Mira
Class: Mage
HP: 24
Level: 3
Mira was added.
```

Choose **2) List roster**. In a new database, the output is:

```text
  [1] Mira - Mage, Level 3, HP 24
```

IDs may differ if the database has been used before. Quit, launch the GUI from the same folder, and the saved character should appear in its table. Select the row and click **Delete Selected** to remove it.

## Skills practiced

| Skill | Where it appears | What I can explain or do |
| --- | --- | --- |
| SQLite table creation | `init_db()` | Define required columns and an automatically generated primary key; create the table only when needed. |
| Parameterized SQL | `add_character()` and `delete_character()` | Pass values separately using `?` placeholders, including a one-item tuple for a deletion ID. |
| Retrieving and displaying data | `list_characters()`, `print_roster()`, and `refresh_list()` | Fetch rows as tuples and display them in terminal output or a Treeview. |
| Persistence and connections | `conn.commit()` and `conn.close()` | Save database changes and close the connection when the application exits normally. |
| Validation and exceptions | Terminal `main()` and GUI `on_add_click()` | Distinguish failed integer conversion from an integer outside the permitted range; reject invalid entries before insertion. |
| Classes and GUI widgets | `RosterApp.__init__()` | Store Entry and Treeview widgets as instance attributes and arrange widgets with `grid()`. |
| Event-driven programming | Button callbacks and `root.mainloop()` | Connect button clicks to methods and refresh displayed data after changes. |
| Record identity | GUI `on_delete_click()` | Retrieve the selected row's database ID so characters with identical names remain distinguishable. |

## Recorded checks

The following results were observed during manual testing:

| Test | Observed result |
| --- | --- |
| Add Mira, list the roster, delete Mira, and list again in the terminal | Mira appeared, deletion succeeded, and the empty-roster message appeared. |
| Close and restart the terminal program | John and Troy remained in the database. |
| Add Finn with HP `0` in the terminal | The program displayed `HP and level must be greater than 0.` and returned to the menu. |
| Delete a nonexistent ID, including `100` | The program displayed `No character was found with that ID.` |
| Open the GUI, delete John and Troy, and add Lucas with valid entries | Existing characters loaded; deletion and addition worked. |
| Attempt to add Kleo with HP `0` in the GUI | A pop-up displayed `HP and level must be at least 1.` |

These observations describe the tested cases, not every possible input. Personal reflections and the full learning journal are submitted separately in Canvas.

## Two known limitations

1. **Database location depends on the working directory.** `DB_FILE = "roster.db"` is a relative path. Launching the programs from different folders can create different databases and make the roster appear missing. Run both from the same activity folder. The programs also do not handle database access failures such as a nonwritable location.
2. **GUI deletion processes only one selected row.** The callback uses `selected[0]`. If several rows are selected, only the first item returned by the selection is deleted. Bulk deletion is not implemented; select one row at a time.

## Repository and submission files

Publish the completed Python source files and this README. Submit the same Python versions to Canvas as the versions committed to Git. Use the instructor-approved repository access settings and provide a direct link to the activity folder.

**Do not submit or publish `roster.db`.** It contains local test data and is created automatically. Also exclude instructor solutions, textbook PDFs, private records, classmates' work, virtual environments, and Python cache files. Keep personal reflections and grade-related documents in Canvas.

Add these patterns to the repository's existing `.gitignore`:

```gitignore
# Local SQLite test data and sidecar files
roster.db
roster.db-*

# Local Python environment and caches
.venv/
venv/
__pycache__/
*.pyc
```

If `roster.db` was already tracked, `.gitignore` alone will not stop tracking it. From the activity folder, use `git rm --cached roster.db`, then commit that removal. This keeps the local database file but removes it from the next repository snapshot; it does not erase earlier commits.

## Credits and AI assistance

The project is based on the course-provided Activity 4 Party Roster Manager starter files and student guide. The GUI database functions reuse the Week 8 database implementation. Character names and attributes are fictional test data; no external dataset is required.

ChatGPT provided some assistance with TODO explanations, menu and callback code, input validation, Treeview refreshing, and troubleshooting path quoting and an unmatched parenthesis.
