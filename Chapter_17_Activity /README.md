# Chapter 17 Activity: The Coffee Cart Ledger

**Course:** MSBA 270 | **Topic:** Working with a database in Python
**Textbook:** *Murach's Python Programming* (2nd ed.), Chapter 17, "How to work with a database," printed pages **470–475, 478–479, 486–494**

A campus coffee cart keeps its menu and orders in a SQL Server database. In about 25 minutes you will finish four small Python functions, make a prediction before each experiment, and then see how the database reacts.

## What you will be able to do afterward

1. **Write a parameterized query** (`?` placeholders plus a tuple) for a `SELECT` and an `INSERT`, and explain why it beats pasting values into the SQL text.
2. **Explain what `commit()` does** and show evidence: an `INSERT` that was executed but never committed disappears when the connection closes.
3. **Explain a foreign key** well enough to predict what the database does when you order an item that doesn't exist.

You will also practice retrieving rows from two related tables (a `JOIN`) and using them in Python.

## Textbook references

| Idea | Pages |
|---|---|
| Tables, primary keys, foreign keys, column definitions | 470–475 |
| `SELECT` with a `JOIN` | 478–479 |
| Connecting from Python | 486–487 |
| `execute()` with `?` placeholders, `fetchone()` / `fetchall()` | 488–491 |
| `INSERT` and `commit()` | 492–493 |
| Database exceptions (and SQLite's foreign-key behavior) | 494 |

## How SQL Server relates to the textbook's SQLite

The concepts are the same: tables, rows, keys, SQL statements, a connection, a cursor, `execute()`, `fetch…()`, and `commit()`. Differences that matter here:

| | Textbook (SQLite) | This activity (SQL Server) |
|---|---|---|
| Where the data lives | A file; `connect("movies.sqlite")` (p. 486–487) | A server process in a Docker container; connect by address, user, and password |
| Python module | `sqlite3`, built in | `mssql-python`, installed with `pip` |
| Placeholders | `?` with a tuple | `?` with a tuple also works with `mssql-python` |
| Generated primary key | DBMS generates it (p. 470) | `IDENTITY(1,1)` column |
| Column types | `TEXT`, `INTEGER`, `REAL` (p. 474) | `NVARCHAR`, `INT`, `DECIMAL` |
| Invalid foreign key | SQLite does not raise an exception (p. 494) | SQL Server **rejects** the row (Stage 3) |
| Row access by name | `conn.row_factory = sqlite3.Row` (p. 491) | Starter converts each row to a dict using `cursor.description` |
| Missing database | `connect()` quietly creates an empty file (p. 494) | Connection error if the server or database isn't there |
| Uncommitted changes | Same rule: not saved until `commit()` | Same rule; also, other connections may *wait* on uncommitted rows |

The textbook skips `CREATE TABLE` (p. 476, DDL). `coffee_cart_setup.sql` supplies it so you can focus on DML.

## Prerequisites (do these before class)

- Python 3.10 or newer, with the VS Code **Python** extension
- Visual Studio Code with the **SQL Server (mssql)** extension (used for the SQL script and for inspecting results)
- Docker Desktop installed and a local SQL Server container created through the extension (steps below)
- macOS only: Homebrew OpenSSL (`brew install openssl`) is listed as a prerequisite for the driver

### Open the activity folder

Choose **File → Open Folder… → `Chapter_17_Activity`**. In the Explorer on the left, click `coffee_cart_setup.sql` to open its editor tab, or expand `code` and click `coffee_cart_starter.py`. Switch between these tabs to execute each file with its own button.

Keep the SQL file in the main folder and the Python file inside `code/`. If downloaded filenames include suffixes such as `(1)`, rename them to the names under **Repository contents** before starting.

### Create the SQL Server container (one time)

1. Install the **SQL Server (mssql)** extension in VS Code.
2. Install Docker Desktop, create an account if you're asked to, and open the app. Leave it running.
3. In VS Code, click the new **SQL Server** icon in the left sidebar.
4. Click **New Deployment** and choose a **local Docker SQL Server container**.
5. Choose the **SQL Server 2025 (latest)** image and enter the **class password: `CoffeeCart#2026`** (it's a throwaway password for a local practice container only).
6. Accept the terms and click **Create Container**.
7. When it finishes, open Docker Desktop and confirm the new container is listed and running. **Note its port**: it appears as `<host port>:1433` (usually `1433:1433`). If another SQL Server container already uses 1433, the extension may choose a different host port such as `1434`. The starter tries ports 1433 to 1436 automatically and prints the one it used. If yours is outside that range, create a `.env` file in the main folder and set `MSSQL_SERVER=127.0.0.1,<your host port>`. If your repository includes `.env.example`, you can copy it to `.env`. To free port 1433, stop an older container you no longer need running.
8. In the extension, connect, open a new query, enter `SELECT @@VERSION;`, and click **Execute**.

### Build the database with SQL (in VS Code)

1. Click `coffee_cart_setup.sql` in the VS Code Explorer to open its editor tab.
2. Connect to your local container (status bar, or the SQL Server sidebar).
3. Clear any text selection and click **Execute** (play icon, top right). The default shortcut is **Cmd+Shift+E** on Mac or **Ctrl+Shift+E** on Windows. Run the whole file so it creates the `CoffeeCart` database, two tables, and sample data.
4. The SQL results panel shows **six menu items and three orders**.
5. In the SQL Server sidebar, refresh the database list if needed, then expand and refresh **CoffeeCart → Tables** to see `MenuItem` and `CartOrder`.

For another look at the menu, open a **new query on CoffeeCart**, enter `SELECT * FROM dbo.MenuItem;`, and click **Execute**. The Python activity works on this same database. Running the setup SQL manually is useful for this inspection step, but **optional for Python to work**: the starter runs the same setup file automatically.

> Apple Silicon Macs: SQL Server 2025 images are x64 only and run under emulation. Ask the presenter if your container won't start.

## Setup (all inside VS Code)

1. **Open the whole folder:** **File → Open Folder…** and choose `Chapter_17_Activity`.
2. **Install the Python extension** if VS Code asks for it.
3. **Create the environment and install the driver:** press **Cmd+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows), run **Python: Create Environment**, choose **Venv**, pick Python **3.10 or newer**, and tick **requirements.txt** when asked which dependencies to install. VS Code then selects that environment for you.
   - If VS Code already offered to create a virtual environment when you opened the folder, say yes and tick `requirements.txt`.
4. **Check which Python the run button uses:** open `code/coffee_cart_starter.py`, then use **Cmd+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows) → **Python: Select Interpreter** → choose the activity's **`.venv`**. If you already have an environment with `mssql-python` installed, you can select that instead. Selecting an interpreter does not install the driver by itself.
5. No password setup is needed when you used the class password. For a different password or port, create an optional `.env` in the main folder and set `MSSQL_SA_PASSWORD=your_container_password` and/or `MSSQL_SERVER=127.0.0.1,your_host_port`. If `.env.example` is available, copy it first. Ensure `.env` and `.venv/` are excluded in `.gitignore` before committing to Git.

The SQL extension's connection profile and Python's connection settings are separate. Confirm they point to the same container, especially if multiple SQL Server containers are running.

<details>
<summary>Terminal alternative (if the buttons don't work)</summary>

From inside the `Chapter_17_Activity` folder:

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate        Mac:  source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use the same Python environment for installation and execution. A "No module named mssql_python" error means the selected Python cannot find the driver: it may be missing or installed in another environment. Select the environment containing the driver before using the run button.
</details>

## Run (with buttons)

**The SQL file:** click `coffee_cart_setup.sql` in the Explorer, connect to your container when prompted, clear any text selection, and click **Execute** (play icon, top right). Refresh **CoffeeCart → Tables** in the SQL Server sidebar. Results appear in the SQL results panel.

**The Python file:** expand `code`, click `coffee_cart_starter.py`, confirm the `.venv` interpreter is selected in the status bar, save, and click **▶ Run Python File** (top right). If a dropdown appears, choose **Run Python File in Terminal**. Output appears in the bottom **Terminal** panel. Write your prediction on paper or say it aloud *before* you click Run; the program prints a `>>> QUESTION:` line for each stage.

You do not need to type a terminal command to launch either file. Python prints its output in the terminal panel. Finish the current run before clicking Run Python File again; to stop a run early, press **Ctrl+C** inside its terminal.

Run it once **before editing anything**. Stage 0 (the menu) should print. That's your early success.

Every Python run rebuilds the sample tables by running `coffee_cart_setup.sql`, so you always start from the same data. To start over, save your edits and click Run Python File again after the current run finishes. Executing the SQL setup separately also resets the data. For the final check of saved orders, use a **new query** instead of rerunning the setup file.

The run button does not guarantee that the terminal's working folder is `code/`; it may start at the workspace root or reuse another terminal location. The supplied `SETUP_SQL` uses `__file__` to find the SQL file one level above the Python file. Keep that line and the folder layout as supplied.

## Activity steps

Open `code/coffee_cart_starter.py` and work in the **STUDENT ZONE**. Full instructions, hints, and checkpoints are in `student_guide.md`.

| Step | You do | You'll see |
|---|---|---|
| 0 | Click **Execute** in the SQL setup, inspect the tables, then **Run Python File** in the unchanged starter | The menu and "Orders on file: 3" |
| 1 | **TODO 1:** `find_item_by_name()` | String-built SQL fails on one name; placeholders handle both |
| 2 | **TODO 2:** `place_order()` INSERT, run, predict | The order counts, then vanishes |
| 3 | **TODO 3:** add one line, rerun | The order survives |
| 4 | Read Stage 3 output | SQL Server rejects an order for item 99 |
| 5 | **TODO 4:** `get_receipt()` JOIN | Receipts for Maya and Priya |
| 6 | Open a **new query on CoffeeCart**, enter `SELECT * FROM dbo.CartOrder;`, and click **Execute** | The saved rows appear in `dbo.CartOrder` |

## Expected results (finished version)

The wording of SQL Server error messages may differ slightly from what's shown here.

```
STAGE 1: Looking up an item by name
Looking up: Cold Brew
  string-built SQL -> found Cold Brew ($3.75)
  placeholder (?)  -> found Cold Brew ($3.75)

Looking up: Baker's Dozen Donut Holes
  string-built SQL -> ERROR: ...Incorrect syntax near 's'.
  placeholder (?)  -> found Baker's Dozen Donut Holes ($5.50)

STAGE 2: Does the order survive?
  Before the order .................. 3
  Right after place_order (same connection) 4
  After reconnecting ................ 4

STAGE 3: An order for an item that doesn't exist
  SQL Server refused the row:
   ...The INSERT statement conflicted with the FOREIGN KEY constraint...

STAGE 4: Receipts built from two related tables
RECEIPT - Maya
  2 x Drip Coffee                    $  5.00
  1 x Blueberry Muffin               $  3.25
  TOTAL                              $  8.25

RECEIPT - Priya
  2 x Oat Milk Latte                 $  9.50
  TOTAL                              $  9.50
```

Before TODO 3, Stage 2 shows `3`, `4`, `3`: the order is lost.

## Connect it to your work

Any program that records transactions (orders, signups, survey responses, inventory) needs these three habits: use placeholders, commit on purpose, and let relationships protect your data. Exercise 17-2 (p. 509) asks you to extend the textbook's Movie List program using the same ideas.

## Repository contents

Open **`Chapter_17_Activity/`** as the workspace folder. Keep these paths together so the starter and illustrated guide can find their supporting files.

| Path inside the folder | Purpose |
|---|---|
| `README.md` | Setup, run buttons, and expected results |
| `student_guide.md` | Illustrated activity instructions |
| `student_guide.pdf` | Printable version of the student guide |
| `facilitator_notes.md` | Presenter notes, answer key, and testing record |
| `coffee_cart_setup.sql` | Database setup; click Execute |
| `coffee_cart_commit_demo.sql` | Optional demo: see commit vs rollback in plain SQL |
| `requirements.txt` | Python driver dependency |
| `code/coffee_cart_starter.py` | Student TODOs; click Run Python File |
| `images/01_tables_and_keys.svg` | Tables and keys diagram |
| `images/02_placeholders.svg` | Placeholder diagram |
| `images/03_commit.svg` | Commit diagram |
| `images/04_big_picture.svg` | Python, VS Code, and SQL Server diagram |

Keep any existing `.env.example` and `.gitignore` files in your repository. The `.venv/` environment is created locally during setup and should not be included in the files you submit.

## Sources and AI assistance

- Textbook: Murach's Python Programming, 2nd ed., Chapter 17 (pages listed above). All code and scenarios here are original.
- Microsoft documentation and the `mssql-python` project on GitHub, for driver installation and connection details.
- VS Code workflow: [Run Python code](https://code.visualstudio.com/docs/python/run), [Python environments](https://code.visualstudio.com/docs/python/environments), and [MSSQL keyboard shortcuts](https://learn.microsoft.com/en-us/sql/tools/visual-studio-code-extensions/mssql/mssql-keyboard-shortcuts?view=sql-server-ver17).
- AI assistance: Claude (Anthropic) helped brainstorm the activity and draft the starter code and documents. *[Presenter: confirm and add what you reviewed, changed, and tested yourself.]*
