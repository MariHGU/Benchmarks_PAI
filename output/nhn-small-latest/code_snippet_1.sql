-- Add new column with desired name
ALTER TABLE table_name ADD COLUMN new_col_name datatype;

-- Copy data from old to new column
UPDATE table_name SET new_col_name = old_col_name;

-- Drop old column
ALTER TABLE table_name DROP COLUMN old_col_name;