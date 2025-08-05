-- First, check the current column definition
DESCRIBE users;

-- Then rename it using CHANGE COLUMN
ALTER TABLE users CHANGE user_email email VARCHAR(255) NOT NULL DEFAULT '';

-- Or if you want to keep the same data type as before:
ALTER TABLE users CHANGE user_email email VARCHAR(255);