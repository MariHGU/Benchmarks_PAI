ALTER TABLE table_name ADD new_col_name INT; -- add new column with new name
UPDATE table_name SET new_col_name = old_col_name;  -- copy data from old to new column
ALTER TABLE table_name DROP COLUMN old_col_name;   -- remove the old column