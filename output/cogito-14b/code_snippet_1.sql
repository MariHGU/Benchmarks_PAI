-- Step 1: Add new column with desired name
ALTER TABLE table_name ADD COLUMN new_col_name datatype;

-- Step 2: Copy data from old column to new column
UPDATE table_name SET new_col_name = old_col_name;

-- Step 3: Drop the old column
ALTER TABLE table_name DROP COLUMN old_col_name;