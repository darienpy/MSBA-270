# Activity 3: RPG Character Forge

## Project purpose

This console lab practices object-oriented programming and text-file storage. A `Character` object stores a name, current HP, maximum HP, level, and inventory. The program displays the character, applies damage, levels up, and saves progress for the next run.

This is a scripted demonstration, not an interactive game. Each run applies 30 damage and then increases the level by one, restoring full health before saving.

## Python and dependencies

- Python 3.6 or later is required for the f-string syntax used in this program.
- Only Python built-ins and the standard library are used. No third-party packages, package installation, or `requirements.txt` are needed.
- Check your installed version with `python3 --version` on macOS or `py --version` on Windows. The minimum version above is a syntax requirement, not a claim that every Python version has been tested.

## Files

Place this README in `activity_3_character_forge` with the following files:

| Path | Purpose |
| --- | --- |
| `README.md` | Project instructions and skills documentation. |
| `code/character_forge_starter.py` | Completed Python program. |
| `character_save.txt` | Optional save data, generated when the program runs successfully from this activity folder. |

No input file is required for the first run. If no save exists, the program creates Hero with 100 HP and level 1.

## Setup and run

Download or clone the repository, then open a terminal in the repository root. On macOS, run:

```bash
cd activity_3_character_forge
python3 code/character_forge_starter.py
```

On Windows, use `py code/character_forge_starter.py` from the activity folder.

The run commands assume the Python file is in the `code` subfolder. If it is directly beside this README, use `python3 character_forge_starter.py` instead.

The relative filename `character_save.txt` is resolved from the terminal's current working directory. Run from a writable project folder. Running from another directory can select a different save file or cause a write error.

## Safe sample data

An optional `character_save.txt` can contain these fictional values, one per line:

```text
Hero
100
1
```

The loader reads name, HP, and level in that order. HP and level must be integer text. Successful saving replaces the file's contents. Back up any progress you want to keep before resetting or testing the save file.

## Skills practiced

| Skill | Application in this project | What I can explain or do |
| --- | --- | --- |
| Classes and objects | `Character` groups attributes and methods. | Create an object and explain how `self` refers to that instance. |
| Attributes and lists | `__init__()` sets character attributes and creates an empty inventory list. | Store separate state for each character. Inventory management is not implemented. |
| Methods and state changes | `take_damage()` changes HP; `level_up()` changes level and restores HP. | Trace how method calls update an object's attributes. |
| Conditional validation | Negative damage is rejected and remaining HP is limited to a minimum of zero. | Use conditions to prevent inappropriate state changes. |
| File input and output | `with open()` writes and reads three lines of character data. | Explain file modes, automatic closing, and the need for matching save/load order. |
| Exception handling | Loading handles missing files, invalid numeric data, and other reading errors. | Distinguish conversion errors from range checks and return `None` to trigger fallback behavior. |
| Text formatting and conversion | F-strings display stats; `int()` restores numeric values read from text. | Format output and explain why saved numeric text needs conversion. |

## Expected output example

With no existing save file, the first run should display:

```text
=== RPG Character Forge ===

No saved character found. Creating a new one!
Name: Hero
HP: 100/100
Level: 1
Inventory: []

Name: Hero
HP: 100/100
Level: 2
Inventory: []


Saved to character_save.txt.
```

The temporary 70 HP is not displayed because leveling up restores health before the second stats display. The next run should load level 2 and finish at level 3.

## Checks to reproduce

These are test instructions and expected behavior, not a record of completed tests.

1. **Ordinary use:** Run without a save file, then run again. Confirm that the first run saves level 2 and the second loads it before advancing to level 3.
2. **Invalid save data:** After backing up the save, replace its HP line with `abc`. Loading should print an invalid-data message and create a new character. A successful save then replaces the invalid data.
3. **Negative damage:** Temporarily call `hero.take_damage(-10)` and compare HP before and after. It should print a rejection message and leave HP unchanged. Remove temporary test code afterward.

Personal test observations and learning reflections are submitted separately in Canvas.

## Known limitations

- Only name, current HP, and level are saved. Inventory is reset to an empty list on loading, and maximum HP is set to the saved current HP. Saving an injured character therefore loses its original maximum HP.
- Invalid numeric save data now triggers fallback instead of an unhandled conversion error, but previous progress is not recovered. A later successful save overwrites the previous file. The fallback message says no save was found even when the file exists but cannot be used.
- Save operations do not have added exception handling. A read-only folder or another writing failure can still stop the program with an `OSError`.
- Loaded integers are not checked for meaningful ranges. Negative HP or levels in a manually edited file can produce inappropriate character state. Damage is expected to be numeric; nonnumeric method arguments are not handled.

## Credits

The project began with the course-provided Activity 3 RPG Character Forge starter. The completed TODOs and journal comments were developed with step-by-step ChatGPT assistance. Meaningful AI help included explanations of attributes and methods, suggested code for saving and loading, troubleshooting a save-location error, and suggestions for damage validation, loading exceptions, and test cases. ChatGPT also helped draft this README.

No external dataset is required; Hero is fictional sample data. Course materials and instructor solutions are not included in this project.
