-- If your original column was INT NOT NULL
ALTER TABLE users CHANGE old_email new_email VARCHAR(255) NOT NULL;

-- If you want to keep the same data type, you can use:
ALTER TABLE users CHANGE old_email new_email VARCHAR(255);