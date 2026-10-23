#!/usr/bin/env python3
"""
Chapter 17 Activity: The Coffee Cart Ledger (STARTER)

A campus coffee cart keeps its menu and orders in SQL Server. Your job is to
finish four small functions and watch what the database does with them.

  TODO 1  find_item_by_name()   SELECT with a ? placeholder
  TODO 2  place_order()         INSERT with ? placeholders
  TODO 3  place_order()         one line: save the change
  TODO 4  get_receipt()         JOIN two related tables

Run the file often:
    python code/coffee_cart_starter.py

The script RESETS the CoffeeCart database (by running coffee_cart_setup.sql) every time it starts, so you can
always try again from a clean state.
"""

import os
import sys
from contextlib import closing

try:
    import mssql_python
except ModuleNotFoundError:
    print("The 'mssql-python' package isn't installed for THIS Python:")
    print(f"  {sys.executable}")
    print("Install it with the same interpreter, then run again:")
    print(f"  {sys.executable} -m pip install mssql-python")
    print("(It needs Python 3.10 or newer. On a Mac you may also need: brew install openssl)")
    sys.exit(1)

# ======================================================================
# SUPPLIED CODE: setup and helpers. Read it, but you don't need to edit it.
# ======================================================================

DB_NAME = "CoffeeCart"

# Class-wide password for the throwaway LOCAL practice container (everyone
# enters this same password when creating the container; see README).
# Never use a password like this for a real database. To use a different
# one, put MSSQL_SA_PASSWORD=... in a .env file (optional).
DEFAULT_CLASS_PASSWORD = "CoffeeCart#2026"

# Docker may map the container to a different port on your computer if 1433
# is already in use. The starter tries these in order and uses the first one
# that connects. (Set MSSQL_SERVER in .env to force a specific address.)
CANDIDATE_SERVERS = ["127.0.0.1,1433", "127.0.0.1,1434",
                     "127.0.0.1,1435", "127.0.0.1,1436"]
ACTIVE_SERVER = CANDIDATE_SERVERS[0]

# The SQL script that builds the database (in the repository's main folder).
SETUP_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "coffee_cart_setup.sql")

# Predict BEFORE you click Run (see the student guide). Run with --pause
# if you also want the program to wait for Enter at each question.
PAUSE_FOR_PREDICTIONS = "--pause" in sys.argv


def load_env_file():
    """Read KEY=value lines from the .env file in the repository root."""
    here = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(here, "..", ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def connect(database=DB_NAME, autocommit=False):
    """Open a connection to the SQL Server running in Docker.

    Unlike SQLite (textbook p. 486-487), there is no database file to point
    at. We connect to a server by address, user name, and password.
    """
    server = os.environ.get("MSSQL_SERVER") or ACTIVE_SERVER
    user = os.environ.get("MSSQL_USER", "sa")
    password = os.environ.get("MSSQL_SA_PASSWORD", DEFAULT_CLASS_PASSWORD)
    conn_str = (
        f"SERVER={server};DATABASE={database};UID={user};PWD={password};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    return mssql_python.connect(conn_str, autocommit=autocommit)


def check_setup():
    """Find a working server address, or fail with a friendly checklist."""
    global ACTIVE_SERVER
    forced = os.environ.get("MSSQL_SERVER")
    candidates = [forced] if forced else CANDIDATE_SERVERS
    last_error = None
    for server in candidates:
        ACTIVE_SERVER = server
        try:
            connect("master").close()
            print(f"Connected to SQL Server at {server}\n")
            return
        except Exception as e:  # any connection failure
            last_error = e
    print("Could not connect to SQL Server. Check that:")
    print("  1. Docker Desktop is open and the SQL Server container is running")
    print("  2. The container's password is the class password (see README)")
    print("     or matches MSSQL_SA_PASSWORD in your optional .env file")
    print("  3. Its port in Docker Desktop (<host>:1433) is listed below;")
    print("     if not, set MSSQL_SERVER=127.0.0.1,<port> in .env")
    print(f"\nTried: {', '.join(candidates)}   user: {os.environ.get('MSSQL_USER', 'sa')}")
    print(f"Last driver message: {short_error(last_error)}")
    sys.exit(1)


def reset_database():
    """Rebuild the database by running coffee_cart_setup.sql.

    This is the 'try again' button. It runs the same script you can run in
    the MSSQL extension. The script is split into batches at each line that
    says GO (GO is a tool command, not SQL, so we handle it here).
    """
    if not os.path.exists(SETUP_SQL):
        print("Can't find coffee_cart_setup.sql. Keep the repository's folder")
        print("layout (the .sql file one level above the code folder) and run")
        print("the starter from there.")
        sys.exit(1)
    with open(SETUP_SQL, encoding="utf-8") as f:
        script = f.read()

    batches, current = [], []
    for line in script.splitlines():
        if line.strip().upper() == "GO":
            batches.append("\n".join(current))
            current = []
        else:
            current.append(line)
    batches.append("\n".join(current))

    # autocommit=True: CREATE DATABASE can't run inside a transaction.
    with closing(connect("master", autocommit=True)) as conn:
        with closing(conn.cursor()) as c:
            for batch in batches:
                if batch.strip():
                    c.execute(batch)


def fetch_all_dicts(cursor):
    """Turn every row in a result set into a dict keyed by column name."""
    names = [col[0] for col in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]


def fetch_one_dict(cursor):
    """Turn the next row into a dict, or return None if there isn't one."""
    row = cursor.fetchone()
    if row is None:
        return None
    names = [col[0] for col in cursor.description]
    return dict(zip(names, row))


def short_error(e):
    """First line of an error message, trimmed so it fits on screen."""
    text = str(e).strip().splitlines()[0] if str(e).strip() else repr(e)
    return text if len(text) <= 200 else text[:200] + "..."


def pause(message):
    """Show the question this experiment answers (you predicted it already)."""
    print(f"\n>>> QUESTION: {message}")
    if PAUSE_FOR_PREDICTIONS:
        input("    (Press Enter to run it.) ")
    print()


def abandon(conn):
    """Close a connection WITHOUT committing, like a program that just ends.

    Drivers normally discard uncommitted work when a connection closes. We
    say rollback() out loud so the demo behaves the same on every machine.
    """
    conn.rollback()
    conn.close()


def list_menu(conn):
    with closing(conn.cursor()) as c:
        c.execute("SELECT itemID, name, price FROM dbo.MenuItem ORDER BY itemID")
        return fetch_all_dicts(c)


def count_orders(conn):
    with closing(conn.cursor()) as c:
        c.execute("SELECT COUNT(*) FROM dbo.CartOrder")
        return c.fetchone()[0]


def find_item_unsafe(conn, name):
    """FOR COMPARISON ONLY. Builds the SQL by pasting the text into it.

    Do not write code like this. Stage 1 shows why.
    """
    query = f"SELECT itemID, name, price FROM dbo.MenuItem WHERE name = '{name}'"
    with closing(conn.cursor()) as c:
        c.execute(query)
        return fetch_one_dict(c)


def describe(item):
    if item is None:
        return "no result (is TODO 1 finished?)"
    return f"found {item['name']} (${item['price']:.2f})"


def print_receipt(customer, lines):
    print(f"RECEIPT - {customer}")
    total = 0
    for line in lines:
        line_total = line["price"] * line["quantity"]
        total += line_total
        print(f"  {line['quantity']} x {line['name']:<28} ${line_total:>6.2f}")
    print(f"  {'TOTAL':<32} ${total:>6.2f}\n")


# ======================================================================
# STUDENT ZONE: complete the four TODOs below.
# Hints: textbook p. 488-489 (placeholders), p. 490-491 (fetch),
#        p. 492-493 (INSERT + commit), p. 478-479 (JOIN).
# ======================================================================

def find_item_by_name(conn, name):
    """Return the menu item with this exact name as a dict, or None."""

    # TODO 1: Write a SELECT that gets itemID, name, and price from
    # dbo.MenuItem WHERE name = ?  (use a ? placeholder, NOT an f-string).
    # Then: execute it with the value in a tuple, e.g. (name,)
    # and return fetch_one_dict(c). Wrap it in:
    #     with closing(conn.cursor()) as c:
    return None


def place_order(conn, item_id, customer, quantity):
    """Add one row to dbo.CartOrder."""

    # TODO 2: Write an INSERT INTO dbo.CartOrder (itemID, customer, quantity)
    # with three ? placeholders, and execute it with a 3-value tuple.
    # Do NOT commit yet! Run the file first and watch Stage 2.

    # TODO 3: After you've seen Stage 2, add ONE line here that saves the
    # change to the database. Then run again and compare.
    pass


def get_receipt(conn, customer):
    """Return one dict per line item for this customer.

    Each dict needs the keys: name, price, quantity.
    """

    # TODO 4: Write a SELECT that JOINs dbo.CartOrder to dbo.MenuItem
    # ON the matching itemID, and returns MenuItem.name, MenuItem.price,
    # and CartOrder.quantity WHERE CartOrder.customer = ?
    # Return fetch_all_dicts(c). (If nothing matches, that's an empty list.)
    return None


# ======================================================================
# SUPPLIED CODE: the experiments that run your functions.
# ======================================================================

def stage_0_menu():
    print("STAGE 0: The menu (supplied code - this should work right away)\n")
    with closing(connect()) as conn:
        for item in list_menu(conn):
            print(f"  {item['itemID']:<3}{item['name']:<28}${item['price']:.2f}")
        print(f"\n  Orders on file: {count_orders(conn)}\n")


def stage_1_lookups():
    print("=" * 60)
    print("STAGE 1: Looking up an item by name\n")
    pause("We'll look up two names, each two ways (4 lookups). "
          "Which lookup(s) do you think will fail?")
    with closing(connect()) as conn:
        for name in ["Cold Brew", "Baker's Dozen Donut Holes"]:
            print(f"Looking up: {name}")
            try:
                print("  string-built SQL ->", describe(find_item_unsafe(conn, name)))
            except mssql_python.Error as e:
                conn.rollback()
                print("  string-built SQL -> ERROR:", short_error(e))
            print("  placeholder (?)  ->", describe(find_item_by_name(conn, name)))
            print()


def stage_2_commit():
    print("=" * 60)
    print("STAGE 2: Does the order survive?\n")
    pause("Priya orders 2 Oat Milk Lattes. The program counts orders before, "
          "right after the INSERT, then reconnects and counts again. "
          "What will the three counts be?")
    cashier = connect()
    before = count_orders(cashier)
    place_order(cashier, 2, "Priya", 2)
    during = count_orders(cashier)
    abandon(cashier)                      # the program 'ends' here

    checker = connect()                   # a brand-new connection
    after = count_orders(checker)
    checker.close()

    print(f"  Before the order .................. {before}")
    print(f"  Right after place_order (same connection) {during}")
    print(f"  After reconnecting ................ {after}\n")
    if during == before:
        print("  Count never changed. Is TODO 2 finished?\n")
    elif after == before:
        print("  The order looked saved, then VANISHED. Why? (TODO 3)\n")
    else:
        print("  The order is still there after reconnecting. It was committed.\n")


def stage_3_foreign_key():
    print("=" * 60)
    print("STAGE 3: An order for an item that doesn't exist\n")
    pause("We'll order item 99, but the menu only has items 1-6. "
          "The textbook says SQLite doesn't raise an error here (p. 494). "
          "What will SQL Server do?")
    with closing(connect()) as conn:
        try:
            place_order(conn, 99, "Ghost", 1)
            print("  No error. (Is TODO 2 finished? Or did the row get in?)\n")
        except mssql_python.Error as e:
            conn.rollback()
            print("  SQL Server refused the row:")
            print("  ", short_error(e), "\n")


def stage_4_receipts():
    print("=" * 60)
    print("STAGE 4: Receipts built from two related tables\n")
    with closing(connect()) as conn:
        for customer in ["Maya", "Priya"]:
            lines = get_receipt(conn, customer)
            if lines is None:
                print(f"  (TODO 4 isn't finished yet - no receipt for {customer})\n")
            elif not lines:
                print(f"  No orders found for {customer}.\n")
            else:
                print_receipt(customer, lines)


def main():
    load_env_file()
    print("=== The Coffee Cart Ledger ===\n")
    check_setup()
    reset_database()
    print("(Database reset to the starting sample data.)\n")

    stage_0_menu()
    stage_1_lookups()
    stage_2_commit()
    stage_3_foreign_key()
    stage_4_receipts()
    print("Done. Open the MSSQL extension in VS Code and run:")
    print("  SELECT * FROM dbo.CartOrder;")


if __name__ == "__main__":
    main()
