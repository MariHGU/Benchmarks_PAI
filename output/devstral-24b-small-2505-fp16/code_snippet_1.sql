-- Step 1: Add a new column with the desired name
ALTER TABLE table_name ADD COLUMN new_col_name datatype;

-- Step 2: Copy data from old column to new column (assuming both columns are of the same type)
UPDATE table_name SET new_col_name = old_col_name;

-- Step 3: Drop the old column
ALTER TABLE table_name DROP COLUMN old_col_name;

-- If needed, rename the new column to the original name:
-- ALTER TABLE table_name CHANGE COLUMN new_col_name old_col_name datatype;