-- Step 1: Create a new table with the desired column names
CREATE TABLE new_table_name LIKE table_name;

-- Step 2: Copy the data from the old table to the new table
INSERT INTO new_table_name SELECT * FROM table_name;

-- Step 3: Drop the old table
DROP TABLE table_name;

-- Step 4: Rename the new table to the original table name
RENAME TABLE new_table_name TO table_name;