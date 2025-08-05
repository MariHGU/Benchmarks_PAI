-- Step 1: Create a new table with the desired column names
CREATE TABLE new_table_name (
    new_col_name1 data_type,
    new_col_name2 data_type,
    -- Add other columns as needed
);

-- Step 2: Copy the data from the old table to the new table
INSERT INTO new_table_name (new_col_name1, new_col_name2)
SELECT old_col_name1, old_col_name2 FROM table_name;

-- Step 3: Drop the old table
DROP TABLE table_name;

-- Step 4: Rename the new table to the original table name
RENAME TABLE new_table_name TO table_name;