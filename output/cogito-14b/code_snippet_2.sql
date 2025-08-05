-- Add new column
ALTER TABLE your_table ADD COLUMN new_column VARCHAR(50);

-- Copy data
UPDATE your_table SET new_column = old_column;

-- Drop old column
ALTER TABLE your_table DROP COLUMN old_column;