ALTER TABLE table_name ADD new_col_name datatype; -- replace 'datatype' with your column type
UPDATE table_name SET new_col_name = old_col_name;
ALTER TABLE table_name DROP COLUMN old_col_name;