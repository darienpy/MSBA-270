/* ==========================================================
   Chapter 17 Activity: The Coffee Cart Ledger
   coffee_cart_setup.sql

   Builds (or rebuilds) the CoffeeCart database with sample data.
   Safe to run again: it drops the two tables and recreates them.

   HOW TO RUN IN VS CODE (MSSQL extension):
     1. Open this file in VS Code.
     2. Connect to your local SQL Server container (status bar or
        "MS SQL: Connect").
     3. Run the whole file (Ctrl+Shift+E / Cmd+Shift+E, or the
        green Execute button).

   The Python starter reads this same file whenever it resets the
   database, so both paths give you identical data.
   ========================================================== */

-- Create the database if it isn't there yet.
IF DB_ID('CoffeeCart') IS NULL
    CREATE DATABASE CoffeeCart;
GO

USE CoffeeCart;
GO

-- Drop the child table (the one with the foreign key) first.
IF OBJECT_ID('dbo.CartOrder', 'U') IS NOT NULL DROP TABLE dbo.CartOrder;
IF OBJECT_ID('dbo.MenuItem',  'U') IS NOT NULL DROP TABLE dbo.MenuItem;
GO

-- Parent table. IDENTITY(1,1): SQL Server generates the primary key (textbook p. 470).
CREATE TABLE dbo.MenuItem (
    itemID INT IDENTITY(1,1) PRIMARY KEY,
    name   NVARCHAR(50) NOT NULL,
    price  DECIMAL(5,2) NOT NULL
);
GO

-- Child table. itemID is a FOREIGN KEY that must match a MenuItem (textbook p. 472).
CREATE TABLE dbo.CartOrder (
    orderID  INT IDENTITY(1,1) PRIMARY KEY,
    itemID   INT NOT NULL REFERENCES dbo.MenuItem(itemID),
    customer NVARCHAR(50) NOT NULL,
    quantity INT NOT NULL
);
GO

-- Sample data. In SQL, a single quote inside text is doubled: 'Baker''s'.
INSERT INTO dbo.MenuItem (name, price) VALUES
    ('Drip Coffee',               2.50),
    ('Oat Milk Latte',            4.75),
    ('Cold Brew',                 3.75),
    ('Chai Latte',                4.25),
    ('Blueberry Muffin',          3.25),
    ('Baker''s Dozen Donut Holes', 5.50);
GO

INSERT INTO dbo.CartOrder (itemID, customer, quantity) VALUES
    (1, 'Maya',   2),
    (5, 'Maya',   1),
    (3, 'Jordan', 1);
GO

-- Quick check: you should see 6 menu items and 3 orders.
SELECT * FROM dbo.MenuItem;
SELECT * FROM dbo.CartOrder;
GO
