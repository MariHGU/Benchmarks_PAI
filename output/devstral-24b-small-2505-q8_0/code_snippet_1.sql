-- Step 1: Create a backup (optional but recommended)
CREATE TABLE backup_table LIKE original_table;
INSERT INTO backup_table SELECT * FROM original_table;

-- Step 2: Create a new table with the same structure as the old one
CREATE TABLE new_table LIKE original_table;

-- Step 3: Alter the new table to rename the column
ALTER TABLE new_table CHANGE COLUMN old_col_name new_col_name data_type;

-- Step 4: Copy the data from the original table to the new table
INSERT INTO new_table SELECT * FROM original_table;

-- Step 5: Drop the old table and rename the new one
DROP TABLE original_table;
RENAME TABLE new_table TO original_table;