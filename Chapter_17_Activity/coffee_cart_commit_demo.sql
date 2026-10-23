/* ==========================================================
   OPTIONAL DEMO: "Executing is not saving" in plain SQL
   (textbook pp. 492-493)

   This creates NO new tables. It only adds, then undoes, one row in
   dbo.CartOrder so you can SEE the pending-change idea.

   Run the whole file with Execute. You'll get three result grids:
     1. orders_at_start               -> 3
     2. orders_inside_transaction     -> 4  (your session sees its own change)
     3. orders_after                  -> 3  (ROLLBACK threw the change away)

   Then change ROLLBACK to COMMIT and run again: orders_after is 4.
   To reset to the original data, run coffee_cart_setup.sql.
   ========================================================== */

USE CoffeeCart;
GO

SELECT COUNT(*) AS orders_at_start FROM dbo.CartOrder;

BEGIN TRANSACTION;

INSERT INTO dbo.CartOrder (itemID, customer, quantity)
VALUES (2, 'Priya', 2);

SELECT COUNT(*) AS orders_inside_transaction FROM dbo.CartOrder;

ROLLBACK TRANSACTION;      -- <<< try changing this line to: COMMIT TRANSACTION;

SELECT COUNT(*) AS orders_after FROM dbo.CartOrder;
GO
