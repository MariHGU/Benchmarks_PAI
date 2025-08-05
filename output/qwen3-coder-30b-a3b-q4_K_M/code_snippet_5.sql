-- Add new column
ALTER TABLE table_name ADD COLUMN new_col_name column_definition;

-- Copy data (if needed)
UPDATE table_name SET new_col_name = old_col_name;

-- Drop old column
ALTER TABLE table_name DROP COLUMN old_col_name;