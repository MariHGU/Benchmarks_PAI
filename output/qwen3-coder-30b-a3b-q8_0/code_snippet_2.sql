-- If your column is INT
ALTER TABLE table_name CHANGE COLUMN old_col_name new_col_name INT;

-- If your column is VARCHAR(255)
ALTER TABLE table_name CHANGE COLUMN old_col_name new_col_name VARCHAR(255);

-- If your column has specific attributes like NOT NULL, DEFAULT, etc.
ALTER TABLE table_name CHANGE COLUMN old_col_name new_col_name VARCHAR(100) NOT NULL DEFAULT '';